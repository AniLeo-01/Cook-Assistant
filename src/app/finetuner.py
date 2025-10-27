import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from datasets import load_dataset, Dataset
from trl import SFTTrainer, SFTConfig
import math
from tqdm import tqdm
from peft import get_peft_model, LoraConfig

MODEL_NAME = "Qwen/Qwen3-0.6B"
MAX_LENGTH = 8192         # set according to model/context available
# IGNORE_INDEX = -100
PER_DEVICE_BATCH_SIZE = 1
GRAD_ACCUM = 8

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, dtype=torch.bfloat16)
# model.unload()

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

dataset = load_dataset('json',
                       data_files = 'instruction_tuned_dataset_processed.jsonl', split='train'
                      )
                      
# Ensure content is string
def ensure_text(example):
    conv = []
    for msg in example["conversations"]:
        content = msg.get("content", "")
        if not isinstance(content, str):
            content = str(content)
        conv.append({"role": str(msg.get("role", "user")), "content": content})
    return {"conversations": conv}

dataset = dataset.map(ensure_text, desc="Normalizing message content")

# Format into a single "text" column using the model's chat template
def format_conversation(example):
    conv = example["conversations"]
    text = tokenizer.apply_chat_template(
        conv,
        tokenize=False,
        add_generation_prompt=False,  # training on full chat
    )
    return {"text": text}

dataset = dataset.map(format_conversation, desc="Formatting conversations -> text")
dataset = dataset.filter(lambda x: isinstance(x["text"], str) and len(x["text"].strip()) > 0)

# SFT training args
training_args = SFTConfig(
    output_dir="./results",
    num_train_epochs=1,
    per_device_train_batch_size=8,  # 32 may OOM for 7B + LoRA; adjust to your GPU
    gradient_accumulation_steps=4,
    gradient_checkpointing=True,
    optim="paged_adamw_8bit",
    learning_rate=1e-5,
    lr_scheduler_type="cosine",
    save_strategy="steps",
    save_steps=500,
    logging_steps=10,
    warmup_ratio=0.03,
    group_by_length=True,
    run_name="cook_assistant_1",
    bf16=True,
    packing=False,
    dataset_text_field="text",           # <-- use the "text" column
    max_length=MAX_LENGTH,
    assistant_only_loss=False,            # <-- now OK: formatted conversational text
    eos_token="<|im_end|>",              # Qwen chat templates use <|im_end|>
    pad_token=tokenizer.pad_token,
)
# --- LoRA Config ---
lora_config = LoraConfig(
    r=4, # Increased rank for potentially better performance
    lora_alpha=16,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=None, # Target more modules
)
model = get_peft_model(model, lora_config)

trainer = SFTTrainer(
    model=model,
    processing_class=tokenizer,
    args=training_args,
    train_dataset=dataset,
    peft_config=lora_config,
)

trainer.train()
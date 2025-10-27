import os
import modal
from dotenv import load_dotenv

vllm_image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install(
        "vllm==0.10.0",
        "huggingface_hub",
        "hf_transfer",
        "bitsandbytes",
    )
    .env({"HF_TOKEN": os.getenv("HF_TOKEN"), "HF_HUB_ENABLE_HF_TRANSFER": "1"})
)

hf_cache_vol = modal.Volume.from_name("model-cache", create_if_missing=True)
vllm_cache_vol = modal.Volume.from_name("vllm-cache", create_if_missing=True)
FAST_BOOT = True

app = modal.App("cook-assistant-v1")

N_GPU = 1  # tip: for best results, first upgrade to more powerful GPUs, and only then increase GPU count
API_KEY = "2is0Irr9q7" # api key, for auth. for production use, replace with a modal.Secret

MINUTES = 60  # seconds

VLLM_PORT = 8000


@app.function(
    image=vllm_image,
    gpu=f"T4:{N_GPU}",
    # how many requests can one replica handle? tune carefully!
    allow_concurrent_inputs=100,
    # how long should we stay up with no requests?
    scaledown_window=15 * MINUTES,
    volumes={
        "/root/.cache/huggingface": hf_cache_vol,
        "/root/.cache/vllm": vllm_cache_vol,
    },
)
@modal.web_server(port=VLLM_PORT, startup_timeout=15 * MINUTES)
def serve():
    import subprocess

    cmd = [
        "vllm",
        "serve",
        "--uvicorn-log-level=info",
        "anileo1/cook-assistant-Qwen3-0.6B",
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
        "--api-key",
        API_KEY,
        "--max-model-len",
        "8192",
    ]
    # enforce-eager disables both Torch compilation and CUDA graph capture
    # default is no-enforce-eager. see the --compilation-config flag for tighter control
    cmd += ["--enforce-eager" if FAST_BOOT else "--no-enforce-eager"]

    # assume multiple GPUs are for splitting up large matrix multiplications
    # cmd += ["--tensor-parallel-size", str(N_GPU)]


    subprocess.Popen(" ".join(cmd), shell=True)

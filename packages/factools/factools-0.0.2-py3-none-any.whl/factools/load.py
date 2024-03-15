from typing import Optional
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


def get_gpu_memory(max_gpus=None):
    """Get available memory for each GPU"""
    gpu_memory = []
    num_gpus = (
        torch.cuda.device_count()
        if max_gpus is None
        else min(max_gpus, torch.cuda.device_count())
    )

    for gpu_id in range(num_gpus):
        with torch.cuda.device(gpu_id):
            device = torch.cuda.current_device()
            gpu_properties = torch.cuda.get_device_properties(device)
            total_memory = gpu_properties.total_memory / (1024**3)
            allocated_memory = torch.cuda.memory_allocated() / (1024**3)
            availabel_memory = total_memory - allocated_memory
            gpu_memory.append(availabel_memory)
    return gpu_memory

def load_vicuna_13b(model_path, device: str, num_gpus: int, max_gpu_memory: Optional[str] = None):
    if device == 'cpu':
        kwargs = {"torch_dtype": torch.float32}
    elif device == 'cuda':
        kwargs = {"torch_dtype": torch.float16}
        if num_gpus != 1:
            kwargs["device_map"] = "auto"
            if max_gpu_memory is None:
                kwargs["device_map"] = "sequential"
                available_gpu_memory = get_gpu_memory(num_gpus)
                kwargs["max_memory"] = {
                    i: str(int(available_gpu_memory[i] * 0.85)) + "GiB"
                    for i in range(num_gpus)
                }
            else:
                kwargs["max_memory"] = {i: max_gpu_memory for i in range(num_gpus)}
    else:
        raise ValueError(f"Invalid device: {device}") 
    tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False)
    model = AutoModelForCausalLM.from_pretrained(model_path, low_cpu_mem_usage=True, **kwargs)
    print('loading model success!!')
    return model, tokenizer
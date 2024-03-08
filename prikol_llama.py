from ctransformers import AutoModelForCausalLM
import time
# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.

start_point = time.time()

# llm = AutoModelForCausalLM.from_pretrained("/home/charslib/Documents/hakathon/RussiaBank/llama/llama.cpp/models/my_model", model_file="llama-2-7b.Q4_K_M.gguf", model_type="llama")
llm = AutoModelForCausalLM.from_pretrained("TheBloke/Llama-2-7B-GGUF", model_file="llama-2-7b.Q4_K_M.gguf", model_type="llama", gpu_layers = 50)

first_point = time.time()

print(llm("AI is going to"))

second_point = time.time()

print(llm("Hello"))

third_point = time.time()

print(first_point - start_point)
print(second_point - start_point)
print(third_point - start_point)

template = (
    "We have provided context information below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "Given this information, please answer the question: {query_str}\n"
)
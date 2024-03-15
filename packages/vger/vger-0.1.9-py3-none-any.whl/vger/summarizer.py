from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import json


class Summarizer:
    def __init__(self):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(
            "microsoft/phi-2", torch_dtype="auto", trust_remote_code=True
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            "microsoft/phi-2", trust_remote_code=True
        )
        self.model.to(self.device)

    def summarize(self, code, size=128):
        inputs = self.tokenizer.encode(
            code, return_tensors="pt", return_attention_mask=False
        ).to(self.device)
        outputs = self.model.generate(
            inputs, max_new_tokens=size, pad_token_id=self.tokenizer.eos_token_id
        )
        return self.tokenizer.decode(outputs[0])


if __name__ == "__main__":
    first_prompt = "Instruct: You are a summarization bot that communicates important details for a highly technical audience. Give as much detail as possible. Do not print any code. Focus on machine learning implementation details. List all model architectures, libraries, data sources, file formats, and security vulnerabilities. Only print natural language summaries. If unable to generate a summary, only return the empty string ''. In five sentences, describe what this user is doing based on this activity:\n"
    meta_prompt = "Instruct: You are a summarization bot that communicates important details for a highly technical audience. Give as much detail as possible. Do not print any code. Focus on machine learning implementation details. List all model architectures, libraries, data sources, file formats, and security vulnerabilities. Only print natural language summaries. Only print a final cumulative summary, don't explain each step. In five sentences, describe what this user is doing based on this activity:\n"
    s = Summarizer()
    with open("../../kaggle/0001/419/1419018.ipynb", "r") as f:
        code = json.load(f)
        code = [c["source"] for c in code["cells"]]  # if c["cell_type"] == "code"
        summaries = ["\n".join(c) for c in code if len(c) > 0]
    results = [s.summarize(first_prompt + c + "Output:") for c in summaries]
    output = [
        r.split("Output:")[-1].replace("<>", "").replace("#", "") for r in results
    ]
    output = "\n".join(output)
    output = output.replace("|endoftext|", "")
    print(
        s.summarize(meta_prompt + output + "\nOutput:", size=1028)
        .split("Output:")[-1]
        .replace("<>", "")
        .replace("#", "")
    )

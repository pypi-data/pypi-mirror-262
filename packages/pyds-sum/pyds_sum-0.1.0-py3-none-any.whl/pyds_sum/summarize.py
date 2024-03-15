from pathlib import Path
import json
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
from typing import List
import argparse


class summarizer:
    def __init__(self):
        model_checkpoint = "jtlucas/pyds_sum"
        self.tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_checkpoint)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def read_and_chunk_ipynb(
        self, path: Path, token_chunk_size: int = 512
    ) -> List[str]:
        """
        Reads Jupyter Notebook (.ipynb) content, extracts code cells, and uses a Hugging Face tokenizer
        to split the code content into chunks of up to token_chunk_size tokens.
        Returns a list of code string chunks for a single file.
        """
        with open(path, "r", encoding="utf-8") as f:
            notebook = json.load(f)

        full_code = ""

        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                source_content = cell["source"]
                if isinstance(source_content, list):
                    cell_code = "".join(source_content)
                else:
                    cell_code = source_content

                if len(cell_code) >= 5:
                    full_code += cell_code + "\n"

        tokens = self.tokenizer.encode(full_code, add_special_tokens=False)
        chunks = []
        for i in range(0, len(tokens), round(0.9 * token_chunk_size)):
            chunk_tokens = tokens[i : i + round(0.9 * token_chunk_size)]
            chunk_string = self.tokenizer.decode(
                chunk_tokens, clean_up_tokenization_spaces=True
            )
            chunks.append(chunk_string)

        return ["summarize: " + c for c in chunks]

    def summarize(self, path: Path) -> str:
        """Summarize a Python file or parses ipynb to python first then summarizes"""
        try:
            input_text = self.read_and_chunk_ipynb(path)
        except:
            raise ValueError("Invalid file type. Please provide a valid .ipynb file")
        preds = []
        for chunked_input in input_text:
            chunk_ids = self.tokenizer.encode(
                chunked_input,
                return_tensors="pt",
                truncation=True,
                padding="max_length",
                max_length=512,
            ).to(self.device)
            output_tokens = self.model.generate(chunk_ids, max_length=128)
            output_text = self.tokenizer.decode(
                output_tokens[0], skip_special_tokens=True
            )
            preds.append(output_text)
        if len(preds) > 1:
            preds = "\n".join(preds)
            if self.tokenizer.encode(preds, return_tensors="pt").size()[1] <= 500:
                chunk_ids = self.tokenizer.encode(
                    "summarize: ```" + preds + "```",
                    return_tensors="pt",
                    truncation=True,
                    padding="max_length",
                    max_length=512,
                ).to(self.device)
                output_tokens = self.model.generate(chunk_ids, max_length=128)
                output_text = self.tokenizer.decode(
                    output_tokens[0], skip_special_tokens=True
                )
            else:
                preds = preds[:250] + preds[-250:]
                chunk_ids = self.tokenizer.encode(
                    "Summarize: ```" + preds + "```",
                    return_tensors="pt",
                    truncation=True,
                    padding="max_length",
                    max_length=512,
                ).to(self.device)
                output_tokens = self.model.generate(chunk_ids, max_length=128)
                output_text = self.tokenizer.decode(
                    output_tokens[0], skip_special_tokens=True
                )
            return output_text
        else:
            return preds[0]


def main(path: Path):
    s = summarizer()
    return s.summarize(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize a ipynb ")
    parser.add_argument("path", type=Path, help="Path to the file to be summarized")
    args = parser.parse_args()
    print(main(args.path))

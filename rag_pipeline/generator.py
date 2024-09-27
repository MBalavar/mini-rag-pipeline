# rag_pipeline/generator.py

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

class Generator:
    def __init__(self, model_name: str = "t5-small"):
        """Initialize the generator with the specified model."""
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Load the tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            #trust_remote_code=False
        )
        
        # Load the model
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name,
            #trust_remote_code=False
        ).to(self.device)
        
        # If the tokenizer does not have a pad_token, set it to eos_token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.model.config.pad_token_id = self.tokenizer.eos_token_id

    def generate(self, prompt: str, max_new_tokens: int = 150) -> str:
        """Generate a response from the provided prompt using the specified model."""
        # Tokenize the input text with attention mask
        encoding = self.tokenizer(
            prompt,
            return_tensors='pt',
            truncation=True,
            padding=True,
            max_length=self.tokenizer.model_max_length
        )
        input_ids = encoding['input_ids'].to(self.device)
        attention_mask = encoding['attention_mask'].to(self.device)

        # Generate output
        outputs = self.model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_new_tokens=max_new_tokens,  # Increased tokens
            num_beams=5,
            temperature=0.0,
            top_k=50,
            no_repeat_ngram_size=2,
            early_stopping=True,
        )
        return self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True
        )
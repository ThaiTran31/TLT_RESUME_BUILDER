from transformers import GPT2Tokenizer, GPT2LMHeadModel
from huggingface_hub import login
from django.conf import settings

class GPT2Generator:
    def __init__(self):
        login(token=settings.HF_AUTH_KEY)
        self.tokenizer = GPT2Tokenizer.from_pretrained('deathkun/professional-summary-suggestion', bos_token='<|startoftext|>', eos_token='<|endoftext|>', pad_token='<|pad|>')
        self.model = GPT2LMHeadModel.from_pretrained('deathkun/professional-summary-suggestion')

    def samples(self, sequences):
        generated = self.tokenizer("<|startoftext|> " + sequences, return_tensors="pt").input_ids
        sample_outputs = self.model.generate(
            generated, do_sample=True, max_length=50, top_p=0.95, temperature=1.9, num_return_sequences=5)
        return sample_outputs


    def generate_sequences(self, sequences):
        sample_outputs = self.samples(sequences)

        outputs = map(lambda sample: self.tokenizer.decode(
            sample, skip_special_tokens=True), sample_outputs)

        return outputs

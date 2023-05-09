import transformers
import torch
import sys
import os
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from django.conf import settings

path = os.path.join(settings.BASE_DIR,
                    './professional_summary/gpt2-finetuning-model')


def samples(sequences, model, tokenizer):
    generated = tokenizer("<|startoftext|> " + sequences,
                          return_tensors="pt").input_ids
    sample_outputs = model.generate(
        generated, do_sample=True, max_length=50, top_p=0.95, temperature=1.9, num_return_sequences=5)
    return sample_outputs


def generate_sequences(sequences):
    tokenizer = GPT2Tokenizer.from_pretrained(path + "", local_files_only=True, bos_token='<|startoftext|>',
                                              eos_token='<|endoftext|>', pad_token='<|pad|>')

    model = GPT2LMHeadModel.from_pretrained(path, local_files_only=True)

    sample_outputs = samples(sequences, model, tokenizer)

    # for i, sample_output in enumerate(sample_outputs):
    #     print("{}: {}".format(i, ))
    outputs = map(lambda sample: tokenizer.decode(
        sample, skip_special_tokens=True), sample_outputs)

    return outputs

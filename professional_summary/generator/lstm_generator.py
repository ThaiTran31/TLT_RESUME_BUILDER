import torch
import json
import sys
import re
import os
from torch.distributions import Categorical
from django.conf import settings

vocab_file_name = os.path.join(
    settings.BASE_DIR, './professional_summary/lstm-language-model/vocab.json')
token_mapping_file_name = os.path.join(
    settings.BASE_DIR, './professional_summary/lstm-language-model/token_mapping.json')
model_file_name = os.path.join(
    settings.BASE_DIR, './professional_summary/lstm-language-model/model_scripted.pt')

unknown_token = "<unk>"
start_token = "<start>"
end_token = "<end>"
unknown_token_index = 0
start_token_index = 1
end_token_index = 2


def sample_next(model, tokens):
    tokens = torch.unsqueeze(tokens, dim=0)
    # print("tokens: ", tokens.size())
    predict = model.forward(tokens)
    predict = torch.squeeze(predict)
    predict = torch.permute(predict, (1, 0))
    # print("predict: ", predict.size())
    next_tokens = Categorical(predict)
    next_tokens = next_tokens.sample()
    # print("next_token: ", next_tokens.size())
    last_token = next_tokens[-1]
    last_tokens = torch.unsqueeze(last_token, 0)
    last_tokens = torch.unsqueeze(last_tokens, 0)
    # print("last_token: ", next_tokens.size())
    cat_tokens = torch.cat((tokens, last_tokens), dim=1)
    # print("cat_tokens: ", cat_tokens.size())
    return cat_tokens[0], last_token


def sample(model, tokens, number_tokens):
    generated_tokens = []
    current_tokens = tokens
    for _ in range(number_tokens):
        current_tokens, next_token = sample_next(model, current_tokens)
        generated_tokens += [next_token]
    return generated_tokens


def tokenize(text):
    text = re.sub('([,;])', r' \1 ', text)
    text = re.sub('  ', ' ', text)
    tokens = text.split(' ')
    if (tokens[-1] == ''):
        return tokens[:-1]
    else:
        return tokens


def vectorize(tokens, vocab):
    int_tokens = []
    int_tokens += [vocab[start_token]]
    for token in tokens:
        int_tokens += [vocab[token]
                       if token in vocab else vocab[unknown_token]]
    return torch.tensor(int_tokens)


def convert_to_text(token_mapping, tokens):
    return str.join(' ', [token_mapping[str(token)] for token in tokens])


def generate_tokens(number_tokens, sequences):
    sequences = start_token + " " + sequences
    tokenized = tokenize(sequences)

    with open(vocab_file_name) as f:
        vocab = json.load(f)

    with open(token_mapping_file_name) as f:
        token_mapping = json.load(f)

    vectorized = vectorize(tokenized, vocab)
    model = torch.jit.load(model_file_name)
    model.eval()

    results = []

    for _ in range(5):
        next_tokens = sample(model, vectorized, number_tokens)
        next_tokens = torch.stack(next_tokens)

        next_sequences = convert_to_text(token_mapping, next_tokens.numpy())

        print(sequences + " " + next_sequences)

        results += [sequences + " " + next_sequences]

    return results

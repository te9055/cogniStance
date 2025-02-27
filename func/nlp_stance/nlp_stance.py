import html_to_json
import pandas as pd
import numpy as np
import torch
from torch.utils.data import DataLoader, SequentialSampler, TensorDataset
from transformers import BertTokenizer, BertForSequenceClassification

from func.utils import get_all_sentences

LOCAL_MODEL_PATH = "./models/c-stance"
MAX_LENGTH = 128
DO_LOWER_CASE = True
EVAL_BATCH_SIZE = 32

AGAINST_LABEL = 0
FAVOUR_LABEL = 1
NEUTRAL_LABEL = 2


def tokenize_row(tokenizer, example, max_length, mask_padding_with_zero=False, pad_on_left=False, pad_token=None,
                 pad_token_segment_id=0):
    if pad_token is None:
        pad_token = tokenizer.convert_tokens_to_ids([tokenizer.pad_token])[0]

    inputs = tokenizer.encode_plus(
        example['Text'],
        example['Target'],
        add_special_tokens=True,
        max_length=max_length,
        truncation=True,
    )
    input_ids, token_type_ids = inputs["input_ids"], inputs["token_type_ids"]
    # The mask has 1 for real tokens and 0 for padding tokens. Only real
    # tokens are attended to.
    attention_mask = [1 if mask_padding_with_zero else 0] * len(input_ids)
    input_len = len(input_ids)
    # Zero-pad up to the sequence length.
    padding_length = max_length - len(input_ids)
    if pad_on_left:
        input_ids = ([pad_token] * padding_length) + input_ids
        attention_mask = ([0 if mask_padding_with_zero else 1] * padding_length) + attention_mask
        token_type_ids = ([pad_token_segment_id] * padding_length) + token_type_ids
    else:
        input_ids = input_ids + ([pad_token] * padding_length)
        attention_mask = attention_mask + ([0 if mask_padding_with_zero else 1] * padding_length)
        token_type_ids = token_type_ids + ([pad_token_segment_id] * padding_length)

    assert len(input_ids) == max_length, "Error with input length {} vs {}".format(len(input_ids), max_length)
    assert len(attention_mask) == max_length, "Error with input length {} vs {}".format(len(attention_mask),
                                                                                        max_length)
    assert len(token_type_ids) == max_length, "Error with input length {} vs {}".format(len(token_type_ids),
                                                                                        max_length)

    return attention_mask, input_ids, input_len, token_type_ids


def tokenize_dataset(data_df, tokenizer, device):
    all_input_ids = []
    all_attention_mask = []
    all_token_type_ids = []
    all_lens = []
    for _, row in data_df.iterrows():
        attention_mask, input_ids, input_len, token_type_ids = tokenize_row(
            tokenizer=tokenizer,
            example=row,
            max_length=MAX_LENGTH
        )

        all_input_ids.append(input_ids)
        all_attention_mask.append(attention_mask)
        all_token_type_ids.append(token_type_ids)
        all_lens.append(input_len)

    # Convert to Tensors and build dataset
    tokenized_dataset = TensorDataset(
        torch.tensor(all_input_ids, dtype=torch.long, device=device),
        torch.tensor(all_attention_mask, dtype=torch.long, device=device),
        torch.tensor(all_token_type_ids, dtype=torch.long, device=device),
        torch.tensor(all_lens, dtype=torch.long, device=device),
    )

    return tokenized_dataset


def get_predictions_for(model, tokenized_dataset):
    # Note that DistributedSampler samples randomly
    eval_sampler = SequentialSampler(tokenized_dataset)
    eval_dataloader = DataLoader(
        tokenized_dataset, sampler=eval_sampler, batch_size=EVAL_BATCH_SIZE
    )

    preds = None
    for step, batch in enumerate(eval_dataloader):
        model.eval()
        with torch.no_grad():
            inputs = {
                'input_ids': batch[0], 'attention_mask': batch[1], 'token_type_ids': batch[2],
            }

            outputs = model(**inputs)
            logits = outputs[0]
        if preds is None:
            preds = logits.detach().cpu().numpy()
        else:
            preds = np.append(preds, logits.detach().cpu().numpy(), axis=0)

    return preds


def run_for_target(full_df, stance_target, tokenizer, model, device):
    # Filter to only the sentences that include the stance target
    # TODO: This could be improved to ensure we don't get a partial match for a word. If the target comes from NER/USAS,
    # we could rely on where those have been identified.
    data_df = full_df[full_df["Text"].str.contains(stance_target)]
    print(data_df)

    if len(data_df) == 0:
        return None

    data_df['Target'] = stance_target

    tokenized_dataset = tokenize_dataset(data_df, tokenizer, device)

    preds = get_predictions_for(model, tokenized_dataset)

    predicted_classes = np.argmax(preds, axis=1)

    return dict(zip(*np.unique(predicted_classes, return_counts=True)))


def run_nlp_stance_on_text(table, dataset_id):
    full_df = pd.DataFrame({"Text": get_all_sentences(dataset_id)})
    print(full_df)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    tokenizer = BertTokenizer.from_pretrained(LOCAL_MODEL_PATH, do_lower_case=DO_LOWER_CASE)
    model = BertForSequenceClassification.from_pretrained(LOCAL_MODEL_PATH)
    model.to(device)

    stance_target_list = [
        row['Word']
        for row in html_to_json.convert_tables(table)[0]
        if 'Word' in row
    ]

    res = []
    for stance_target in stance_target_list:
        predicted_counts = run_for_target(full_df, stance_target, tokenizer, model, device)

        if predicted_counts:
            print(predicted_counts)

            total = sum(predicted_counts.values())
            res.append(
                {
                    "0 Word": stance_target,
                    "1 Favour (%)": predicted_counts.get(FAVOUR_LABEL, 0) * 100 / total,
                    "2 Neutral (%)": predicted_counts.get(NEUTRAL_LABEL, 0) * 100 / total,
                    "3 Against (%)": predicted_counts.get(AGAINST_LABEL, 0) * 100 / total,
                }
            )

    print(res)
    return {'output': res, 'message': 'Done', 'code': 'SUCCESS'}


if __name__ == "__main__":
    print(run_nlp_stance_on_text(["中国"], 6))

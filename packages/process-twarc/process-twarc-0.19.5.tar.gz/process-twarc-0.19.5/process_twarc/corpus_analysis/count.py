import itertools
from process_twarc.util import get_output_path, load_dataset, get_files, save_to_parquet
import pandas as pd
import re
from nltk import FreqDist
from tqdm import tqdm
import os
from itertools import chain

def sort_by_value(dict, reverse=True):
    """Returns a dictionary sorted by value. Defaults to reverse order"""
    return {k:v for k,v in sorted(dict.items(), key=lambda item: item[1], reverse=reverse)}

def count_characters(
        file_path: str, 
        output_dir: str=""
        ):
    """
    For decision-making purposes.

    The tokenizer cannot include all characters present in the dataset.

    This function counts the number of Tweets in which each character appears at least once.

    Args:
        file_path (str): Path to a dataset.
        output_dir (str, optional): Path to a directory where the output will be saved.

    Returns:
        character_counts (dict): A dictionary of characters and their counts.
    """
    dataset = load_dataset(file_path, output_type="Dataset", columns="text")
    unique_characters = lambda text: list(set(text))
    character_sets = list(map(unique_characters, dataset["text"]))
    character_sets = itertools.chain.from_iterable(character_sets)
    character_counts = FreqDist(character_sets)
    result = pd.DataFrame(character_counts.items(), columns=["character", "count"])
    result = result.sort_values(by="count", ascending=False)
    if output_dir:
        path_to_output = get_output_path(file_path, output_dir, file_type="csv")
        result.to_csv(path_to_output, index=False)
    return result

def character_count_pipeline(
        data_dir: str,
        intermediate_dir: str,
        output_dir: str
):
    """Pipeline that will count characters by file, and then combine files."""

    files = get_files(data_dir)
    for file in tqdm(files, desc="Counting characters"):
        count_characters(file, intermediate_dir)

    print("All characters counted. Combining counts.")
    results = pd.concat([pd.read_csv(file) for file in get_files(intermediate_dir)])
    results = results.groupby("character").sum().reset_index()
    results = results.sort_values(by="count", ascending=False)
    results.to_csv(os.path.join(output_dir, "character_counts.csv"), index=False)
    return results

def extract_tags(
        file_path: str,
        tag_type: str,
        output_dir: str=""
        ):
    """
    For corpus analysis.

    This functions extracts a tag of choice and writes the results to a file.

    Args:
        file_path (str): Path to a dataset.
        output_dir (str, optional): Path to a directory where the output will be saved.

    Returns:
        hashtags (pd): A dataframe of tags and their counts.
    """
    if tag_type not in ["hashtags", "mentions"]:
        raise ValueError("tag_type must be either 'hashtags' or 'mentions'.")
    if tag_type == "hashtags":
        pattern = r"#\w+"
    elif tag_type == "mentions":
        pattern = r"@\w+"
    dataset = load_dataset(file_path, output_type="Dataset", columns="text")
    tags = list(itertools.chain.from_iterable([re.findall(pattern, text) for text in dataset["text"]]))
    result = pd.DataFrame(FreqDist(tags.items(), columns=["tag", "count"]))
    result = result.sort_values(by="count", ascending=False)
    if output_dir:
        path_to_output = get_output_path(file_path, output_dir, file_type="csv")
        result.to_csv(path_to_output, index=False)

def tag_extraction_pipeline(
        tag_type: str,
        data_dir: str,
        intermediate_dir: str,
        output_dir: str
        ):
    
    """Pipe that will count the selected tag by file, then combine all files."""

    if tag_type not in ["hashtags", "mentions"]:
        raise ValueError("tag_type must be either 'hashtags' or 'mentions'.")
    
    files = get_files(data_dir)
    for file in tqdm(files, desc= f"Extracting {tag_type}"):
        extract_tags(file, tag_type, intermediate_dir)

    print(f"All {tag_type}s counted. Combining counts")

    results = pd.concat([pd.read_csv(file) for file in get_files(intermediate_dir)])
    results = results.groupby("tag").sum().reset_index()
    results = results.sort_values(by="count", ascending=False)
    results.to_csv(os.path.join(output_dir, f"{tag_type}.csv"), index=False)
    return results

def tokenize_for_counting(
        file_path: str,
        tokenizers: dict, 
        tokenized_dir: str,
        masks: list = ["duplicate", "pattern"]
        ):
    
    """Tokenize function that will generate tokenized lists for all experimental tokenizers.
    Also generates a column with a set of all tokens, which is useful for looking for examples of 
    tokens in the corpus."""

    dataset = load_dataset(
        file_path,
        output_type="Dataset",
        columns=["tweet_id", "text", "user_cap"],
        masks=masks
    )

    bert_tokenize_fn = lambda name, example: {f"{name}_tokens": tokenizer.tokenize(example["text"])}
    mecab_tokenize_fn = lambda name, example: {f"{name}_tokens": [word.surface for word in tokenizer(example["text"])]}

    for name, tok_data in tokenizers.items():
        tok_type = tok_data["type"]
        tokenizer = tok_data["tokenizer"]

        tokenize_fn = bert_tokenize_fn if tok_type == "bert" else mecab_tokenize_fn
        dataset = dataset.map(tokenize_fn(name))

    def aggregate_tokens(row):
        columns = [f"{name}_tokens" for name in tokenizers.keys()]
        tokens = list(set(chain(*[row[col] for col in columns])))
        return {"all_tokens": tokens}
    
    dataset = dataset.map(aggregate_tokens)
    path_to_output = get_output_path(file_path, tokenized_dir)
    save_to_parquet(dataset, path_to_output)

def token_count_pipeline(
        tokenized_dir: str,
        tokenizers: dict,
        tokenized_counts_dir: str,
        output_dir: str
):
    """Pipeline that will count tokenized lists by file and then combine tokens for each experimental tokenizer."""
    last_tok = tokenizers.keys()[-1]
    files = get_files(tokenized_dir, remainder=True, output_dir=os.path.join(tokenized_counts_dir, last_tok))

    for file in tqdm(files, desc="Counting tokens."):
        dataset = load_dataset(file)

        for name, tok_data in tokenizers.items():
            if tok_data["user_cap"]:
                dataset = dataset[~dataset["user_cap"]]

            tokens = list(chain(*dataset[f"{name}_tokens"].tolist()))
            freqs = FreqDist(tokens)
            result = pd.DataFrame(freqs, columns=["token", "count"])

            result_dir = os.path.join(tokenized_counts_dir, name)
            os.makedirs(result_dir, exist_ok=True)

            path_to_output = get_output_path(file, result_dir)
            save_to_parquet(result, path_to_output)
    
    print("All tokens counted. Combining counts")

    for name in tokenizers.keys():
        files = get_files(os.path.join(tokenized_counts_dir, name))
        result = pd.concat([load_dataset(file) for file in file]).groupby("token").sum().reset_index
        path_to_output = os.path.join(output_dir, f"{name}_token_counts.csv")
        result.to_csv(path_to_output)
    

        





def find_kaomoji(
        example: list, 
        tokenizer_dict: dict,
        vocab_table: pd.DataFrame):
    vocab = vocab[["token", "char_family"]]
    target = vocab[vocab["char_family"].isin(["SYMBOL", "PUNCTUATION", "SCRIPT"])]["token"].tolist()


    start_idx = None
    count = 0
    chains = []

    name, bert_tokenizer = tokenizer_dict
    tokenized = list(enumerate([True if token in target else False for token in example[name]]))
    chains = []
    for idx, is_true in tokenized:
        if is_true==True:
            count += 1
            if start_idx is None:
                start_idx = idx
            if count >= 5 and idx == len(tokenized) - 1:
                chains.append((start_idx, idx))
        else:
            if count >= 5:
                chains.append((start_idx, idx - 1))
            start_idx = None
            count = 0
     
    encoded = [bert_tokenizer.encode(example[name][start:end+1])[1:-1] for start, end in chains]
    kaomoji = [bert_tokenizer.decode(encoded).replace(" ", "") for encoded in encoded]
    return {f"{name}_kaomoji": kaomoji}
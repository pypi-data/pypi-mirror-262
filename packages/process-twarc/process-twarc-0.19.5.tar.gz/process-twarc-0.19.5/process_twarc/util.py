import pandas as pd
from datasets import Dataset, concatenate_datasets
import pyarrow as pa
import pyarrow.parquet as pq
from tqdm import tqdm
from ntpath import basename
import os
import json
from typing import Union
import webbrowser

def get_file_type(file_path):
    """
    Get the file type from the file path.

    Args:
        file_path (str): The file path.

    Returns:
        str: The file type.
    """
    return file_path.split(".")[-1]

def get_files(directory, remainder=False, output_dir=None, smallest=False):
    """
    Get a list of all files from all directories within the specified directory.

    Args:
        directory (str): The directory containing multiple directories.

    Returns:
        list: A list of file paths from all directories within the specified directory.
    """
    def _get(directory):
        file_list = []
        for root, _, files in os.walk(directory):
            for file in files:
                file_list.append(os.path.join(root, file))
        return file_list
    
    files = _get(directory)
    if remainder:
        if not output_dir:
            raise ValueError("Please provide an output directory.")
        finished = _get(output_dir)
        base = lambda file_path: basename(file_path).split(".")[0]
        files = [f for f in files if base(f) not in [base(f2) for f2 in finished]]
    if smallest:
        sized_files = [(file_path, os.path.getsize(file_path)) for file_path in files]
        sized_files.sort(key=lambda x: x[1])
        files = [file[0] for file in sized_files]
    return files

def load_parquet(file_path: str, output_type: str = "pd", columns=None):
    """
    Load a data structure of the selected type from a parquet file.

    Args:
        file_path (str): Path to the parquet file.
        output_type (str, defaults to "pd"): Type of the output data structure. Either "pd" for pandas DataFrame or "Dataset" for custom Dataset.
        columns (str or list, optional): Columns to load. If provided, only load the specified columns.

    Returns:
        object: Loaded data structure.
    """
    if isinstance(columns, str):
        columns = list(columns)

    if output_type == "pd":
        if columns:
            dataset = pd.read_parquet(file_path, columns=columns)
        else:
            dataset = pd.read_parquet(file_path)
    elif output_type == "Dataset":
        if columns:
            table = pq.read_table(file_path, columns=columns)
        else:
            table = pq.read_table(file_path)
        dataset = Dataset(table)
    else:
        raise ValueError("Please input a valid output type. Either 'pd' or 'Dataset'.")

    return dataset

def merge_lists(*args):
    """Helper function for load_dataset"""
    merged_list = [element for arg in args for element in arg]
    return list(set(merged_list))

def load_dataset(file_path: str, output_type: str = "pd", columns=None, masks=None, drop_mask_columns=True):
    """
    Load a data structure of the selected type from a parquet file and apply optional masking.

    Args:
        file_path (str): Path to the parquet file.
        output_type (str, defaults to "pd"): Type of the output data structure. Either "pd" for pandas DataFrame or "Dataset" for custom Dataset.
        columns (str or list, optional): Columns to load. If provided, only load the specified columns.
        masks (str or list, optional): Mask column(s) to apply and remove rows where the mask is True.

    Returns:
        object: Loaded data structure.
    """
    if columns and isinstance(columns, str):
        columns = [columns]
    
    if masks:
        if isinstance(masks, str):
            masks = [masks]
        if masks and columns:
            columns = list(set(columns+masks))
        
        load_type = "pd"
        dataset = load_parquet(file_path, load_type, columns)
        mask = dataset[masks].any(axis=1)
        dataset = dataset[~mask].reset_index(drop=True)

        if drop_mask_columns:
            dataset = dataset.drop(columns=masks)

        if output_type == "Dataset":
            dataset = Dataset(pa.Table.from_pandas(dataset))
        return dataset

    else:
        dataset = load_parquet(file_path, output_type, columns)
        return dataset


def concat_dataset(file_paths, output_type="pd", columns=None, masks=None, drop_mask_columns=True):
    """
    Concatenate multiple datasets from parquet files and apply optional masking.

    Args:
        file_paths (list[str]): Paths to the parquet files.
        output_type (str, defaults to "pd"): Type of the output data structure. Either "pd" for pandas DataFrame or "Dataset" for custom Dataset.
        columns (str or list[str], optional): Columns to load. If provided, only load the specified columns.
        masks (str or list[str], optional): Mask column(s) to apply and remove rows where the mask is True.

    Returns:
        object: Concatenated and optionally masked data structure.
    """
    datasets = []
    
    for file_path in tqdm(file_paths, desc = "Loading dataset"):
        dataset = load_dataset(file_path, output_type, columns, masks, drop_mask_columns)
        datasets.append(dataset)
    
    concatenated = pd.concat(datasets) if output_type == "pd" else concatenate_datasets(datasets)
    
    return concatenated

def get_output_path(file_path:str, output_dir:str, file_type:str=""):
    """
    Generate a new file path for transforming data from one filetype to another.

    Given the original file path and the destination folder, generate a new file path
    with the destination folder and the specified file type.

    Args:
        file_path (str): The original file path.
        output_dir (str): The destination folder where the transformed file will be saved.
        file_type (str, Optional): The desired file type for the transformed file.

    Returns:
        str: The new file path with the destination folder and file type.
    """
    if file_type:
        file = basename(file_path).split(".")[0]
        ouput_path = f"{output_dir}/{file}.{file_type}"
    else:
        file = basename(file_path)
        ouput_path = f"{output_dir}/{file}"
    return ouput_path

def save_to_parquet(data, file_path):
    if isinstance(data, pd.DataFrame):
        data.to_parquet(file_path)
    elif isinstance(data, Dataset):
        data_frame = pd.DataFrame(data)
        data_frame.to_parquet(file_path)
    else:
        raise ValueError("Data must be either a pd.DataFrame or a HuggingFace Dataset.")
    
def save_dict(dict:dict, save_path: str):
    """
    Save a dictionary to the JSON file format.

    Args:
        dict (dict): Dictionary to be saved.
        save_path (str): Path where the JSON file will be saved.
    """
    with open(save_path, 'w', encoding="utf-8") as f:
        json.dump(dict, f, ensure_ascii=False, indent=2)
        return


def load_dict(path_to_dict: str):
    """Loads a dictionary from a JSON file."""
    with open(path_to_dict, "r", encoding="utf-8") as f:
        return json.load(f)

def find_examples(
        token_sets_dir: str,
        tokens: Union[str, list[str]], 
) -> dict[str, pd.DataFrame]:
    """Provided a directory to a set of tokenized datasets, find examples of tweets containing the specified tokens."""
    dataset = concat_dataset(
        get_files(token_sets_dir),
        columns = ["tweet_id", "tokens"]
    )

    if isinstance(tokens, str):
        tokens = [tokens]
    return {token: dataset[dataset["tokens"].apply(lambda x: token in x)] for token in tokens}

def display_examples(
        examples: dict[str, pd.DataFrame],
        n = 10
):
    """Display a random sample of n tweets from each token set."""
    sample = examples.sample(n)
    for tweet in sample["tweet_id"].tolist():
        webbrowser.open(f"https://twitter.com/anyuser/status/{tweet}")





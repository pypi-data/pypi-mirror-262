import pandas
import json
import itertools
import numpy as np
from tqdm import tqdm


def load_char_list(path):
    """Load hierarchical list of characters and aliases.

    Parameters
    ----------
    path: str
        The path of the clean list of desired characters.
    """
    with open(path, "r", encoding="utf-8") as file:
        temp_list = file.read().splitlines()
    char_list = []
    current = None
    for char in temp_list:
        if "#" in char:
            char = char[: char.index("#")]
        char = char.rstrip()
        if not char:
            continue
        if char.startswith(" "):
            current.append(char.lstrip())
        else:
            current = [char]
            char_list.append(current)
    return char_list



def find_alias(name, char_list):
    """Find all candidates in the list of characters for a given entity"""
    char_aliases = []
    for l in char_list:
        if name in l:
            char_aliases.append(l)
        else:
            for alias in l:
                if name in alias:
                    char_aliases.append(l)
                    break
    return char_aliases


def map_names(df, char_list):
    """For each entry of the dataframe, find the best candidate within the possible characters. Returns the list of mapped names, and the DataFrame with a new column "alias" associating to each entry the corresponding mapped name.
    
    Parameters
    ----------
    df: pandas.DataFrame
        The dataframe of all named entities occurrences.
    char_list: list
        The clean list of all desired characters.
    """
    df["alias"] = ""
    position_dict = dict()
    for idx in df.index:
        name = df.loc[idx]["name"]
        position = df.loc[idx]["start_pos"]

        position_dict[name] = position
        aliases = find_alias(name, char_list)

        if len(aliases) == 1:
            df.at[idx, "alias"] = aliases[0][0]
        elif len(aliases) > 1:
            filtered_dict = dict()
            for l in aliases:
                try:
                    filtered_dict[l[0]] = position_dict[l[0]]
                except:
                    pass

            if filtered_dict:
                closest_alias = max(filtered_dict, key=lambda k: filtered_dict[k])
                df.at[idx, "alias"] = closest_alias
            else:
                df.at[idx, "alias"] = aliases[0][0]
        else:
            df.at[idx, "alias"] = ""
    return df
    
    
def filter_df(df, start, end):
    """Filter dataframe of occurrences by position interval in the text"""
    filtered_df = df[(start <= df["block"]) & (df["block"] < end)]
    filtered_df = filtered_df[filtered_df["alias"]!=""]
    return filtered_df


def create_pairs(df):
    """Combine all possible pairs (cooccurrences) within a group of lines"""
    characters = np.unique(df["alias"])
    if len(characters) > 1:
        combs = itertools.combinations(characters, 2)
        for comb in combs:
            yield comb
    else:
        pass


def find_pairs(char_df, char_list, blocks_size):
    """Find cooccurrences over the entire dataframe.

    Parameters
    ----------
    char_df: pandas.DataFrame
        The dataframe of all named entities occurrences.
    char_list: List
        The clean list of all desired characters.
    blocks_size: int
        Size of each batch (of paragraphs or scenes) to find cooccurrences.
    """

    # Compute number of blocks (depending on chosen blocks size) and round it up
    nb_par = char_df.iloc[-1]["block"]
    nb_blocks = nb_par // blocks_size + (nb_par % blocks_size > 0)

    pairs = []
    start = 0
    
    if not 'alias' in char_df.columns:
        print('no alias preprocessed')
        char_df = map_names(char_df, char_list)

    for i in tqdm(range(nb_blocks)):
        end = start + blocks_size
        filtered_df = filter_df(char_df, start, end)
        for pair in create_pairs(filtered_df):
            pairs.append(pair)
        start = end

    return pairs

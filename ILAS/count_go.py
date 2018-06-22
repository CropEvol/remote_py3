import pandas as pd

def count_go(df):
    # All Go terms put into one list, "all_GO".
    # Some GO terms are duplicated in the "all_GO".
    all_GO = []
    for each_GOs in df["GO"]:
        GO_list = each_GOs.split(",")
        all_GO.extend(GO_list)

    # Counting GO terms using Pandas series
    result = pd.Series(all_GO).value_counts()

    return pd.DataFrame(result, columns=['count'])

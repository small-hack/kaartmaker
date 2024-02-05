from kaartmaker.constants import PWD
import pandas as pd
from os import path

PALESTINE_CSV = path.join(PWD, 'datasets/UN_general_assembly/world_palestine_votes.csv')

def process_csv(data_frame: pd.DataFrame, dataset_csv_file: str = ""):
    """
    take dataframe and process a process csv into it
    fields: NAME_EN, vote, suspended_unrwa_aid
    """
    if not dataset_csv_file:
        dataset_csv_file = PALESTINE_CSV

    df = pd.read_csv(dataset_csv_file, index_col="NAME_EN")

    # update the geojson with cease fire info
    for index, row in df.iterrows():
        vote = row["vote"]

        if vote == "ABSTENTION":
            data_frame.loc[data_frame.NAME_EN == index, "color"] = "#999999"
            data_frame.loc[data_frame.NAME_EN == index, "vote"] = "ABSTENTION"
        elif vote == "IN FAVOR":
            data_frame.loc[data_frame.NAME_EN == index, "color"] = "#648FFF"
            data_frame.loc[data_frame.NAME_EN == index, "vote"] = "IN FAVOR"
        elif vote == "AGAINST":
            data_frame.loc[data_frame.NAME_EN == index, "color"] = "#FFB000"
            data_frame.loc[data_frame.NAME_EN == index, "vote"] = "AGAINST"

    return data_frame

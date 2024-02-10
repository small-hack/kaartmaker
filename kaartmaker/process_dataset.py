from kaartmaker.constants import PWD
import pandas as pd
from os import path

PALESTINE_CSV = path.join(PWD, 'datasets/UN_general_assembly/world_palestine_votes.csv')


def process_csv(data_frame: pd.DataFrame,
                dataset_csv_file: str = "",
                reverse_colors: bool = False,
                sub_units: bool = False):
    """
    take dataframe and process a process csv into it
    fields: NAME_EN, vote, suspended_unrwa_aid
    """
    if not dataset_csv_file:
        dataset_csv_file = PALESTINE_CSV

    df = pd.read_csv(dataset_csv_file, index_col="NAME_EN")

    if not reverse_colors:
        no_color = "#FFB000"
        yes_color = "#648FFF"
    else:
        no_color = "#648FFF"
        yes_color = "#FFB000"

    if sub_units:
        data_frame = color_votes_based_on_sub_unit(df, data_frame, yes_color, no_color)
    else:
        data_frame = color_votes(df, data_frame, yes_color, no_color)

    return data_frame


def color_votes_based_on_sub_unit(df, data_frame, yes_color, no_color):
    # update the geojson with cease fire info
    for index, row in df.iterrows():
        vote = row["vote"]

        if vote == "ABSTENTION":
            data_frame.loc[data_frame.NAME_EN == index, "color"] = "#999999"
        elif vote == "IN FAVOR" or vote == "YES":
            data_frame.loc[data_frame.NAME_EN == index, "color"] = yes_color
        elif vote == "AGAINST" or vote == "NO":
            data_frame.loc[data_frame.NAME_EN == index, "color"] = no_color
        else:
            vote = "ABSENT"

        data_frame.loc[data_frame.NAME_EN == index, "vote"] = vote

    return data_frame


def color_votes(df, data_frame, yes_color, no_color):
    # update the geojson with cease fire info
    for index, row in df.iterrows():
        vote = row["vote"]

        if vote == "ABSTENTION":
            data_frame.loc[data_frame.SOVEREIGNT == index, "color"] = "#999999"
        elif vote == "IN FAVOR" or vote == "YES":
            data_frame.loc[data_frame.SOVEREIGNT == index, "color"] = yes_color
        elif vote == "AGAINST" or vote == "NO":
            data_frame.loc[data_frame.SOVEREIGNT == index, "color"] = no_color
        else:
            vote = "ABSENT"

        data_frame.loc[data_frame.SOVEREIGNT == index, "vote"] = vote

    return data_frame

import pytest
import pandas as pd
from photo_processor import organise


@pytest.fixture
def mapping_data():
    data = {
        "group": ["tatawa", "batu", "makassar"],
        "folder": ["tatawa", "batu", "makassar"],
        "start_time": pd.to_datetime(
            [None, "2020-01-02 10:40:00", "2020-01-02 10:50:00"]
        )
    }
    
    df = pd.DataFrame(data)
    df = organise.prepare_df(df)
    
    return df




cases = [
    ("2020-01-02 10:39:00", "tatawa"),
    ("2020-01-02 10:41:00", "batu"),
    ("2020-01-02 10:51:00", "makassar")
]


@pytest.mark.parametrize("time,expected", cases)
def test_folder_finder(mapping_data, time, expected):
    
    df = mapping_data
    folder = organise.get_folder(pd.to_datetime(time), df)
    
    assert folder == expected

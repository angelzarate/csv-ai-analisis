import pytest
from pathlib import Path
from app.data_driver.csv_data import CSVDataDriver

storage_path = Path("storage").absolute()


@pytest.mark.parametrize(
        "file, total_row", 
        [
            ("dump/data.csv", 1000),
            # ("dump/dataset.csv",  5)            
        ],
)
def test_read(file, total_row):    
    csv_driver = CSVDataDriver(
        storage_path / file
    )
    assert csv_driver.total_rows == total_row
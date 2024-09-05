import pytest

from pathlib import Path
this_directory = Path(__file__).parent.parent

import sys
sys.path.append(str(this_directory))

from ChasmSystem import Entity
from ChasmSystem import Fetcher_Functions as ff

@pytest.fixture()
def ent_data():
    "Fixture for test entity"
    
    return Entity() \
    .set_attribute('Vit', 10) \
    .set_attribute('Str', 15) \
    .return_data()

def test_fetch_attributes(ent_data):
    "Testing fetch_attributes function"

    assert ff.fetch_attribute(ent_data, 'Vit', 'Vit', 'Str') == (10, 10, 15)

def test_add_numbers(ent_data):
    "Testing add_numbers function"

    assert ff.add_numbers(ent_data, 3, 5) == (3, 5)
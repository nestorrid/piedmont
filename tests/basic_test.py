import pytest
from piedmont import Piedmont


def test_start_connection():
    pie = Piedmont('config.yaml')

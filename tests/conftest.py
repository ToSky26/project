import pytest
import requests
from faker import Faker


@pytest.fixture(scope='session')
def base_url():
    return 'https://automation.tivaliclub.com/fcle'


@pytest.fixture(scope='class')
def session():
    with requests.Session() as session:
        yield session


@pytest.fixture
def fake():
    return Faker()

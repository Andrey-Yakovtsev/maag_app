import pytest


pytestmark = pytest.mark.django_db

@pytest.fixture
def mcc_with_all_fks():
    ...

def test_mcc_gets_deleted_fks():
    ...

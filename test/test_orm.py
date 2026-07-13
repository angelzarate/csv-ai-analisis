import pytest
from app.core.database import DatabaseConnection
from app.repositories.requisition_repository import RequesitionRepository

session = DatabaseConnection().session
req_repo = RequesitionRepository(session=session())

@pytest.mark.parametrize(
    "id_solicitud, exists", 
    [
        ("A0001", False),
        ("A001", True), 
        ("A005", True)
    ],
)
def test_exists_requisition(id_solicitud, exists):
    assert req_repo.requisition_exist(id_solicitud=id_solicitud) == exists

@pytest.mark.parametrize(
    "ids, results", 
    [
        (["A0002", "A005", "A001"], ["A005", "A001"])
    ]
)
def test_array_exists(ids: list[str],  results: list[str]):
    set_ids = list(set(ids))    
    _result_ = req_repo.requistions_exist(set_ids)
    assert set(_result_) == set(results)
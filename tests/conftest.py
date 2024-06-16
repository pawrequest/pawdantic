import pytest
from sqlmodel import SQLModel, Session, create_engine

from tests.models import Alert, AlertType, TestModel, TestModelOptionalJson, TestModelRequiredJson

DB_FILE = 'sqlite:///test.db'
DB_MEMORY = 'sqlite:///:memory:'


@pytest.fixture(scope='function')
def test_session():
    engine = create_engine(DB_MEMORY)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def alert_fxt():
    return Alert(message='Test message', type=AlertType.WARNING)


@pytest.fixture
def test_model(alert_fxt):
    return TestModel(
        alert=alert_fxt,
        alerts_list=[alert_fxt],
        alerts_dict={"alert1": alert_fxt},
        alerts_tuple=(alert_fxt, alert_fxt),
    )


@pytest.fixture
def test_model_required_json(alert_fxt):
    return TestModelRequiredJson(
        alert=alert_fxt,
        alerts_list=[alert_fxt],
        alerts_dict={"alert1": alert_fxt},
        alerts_tuple=(alert_fxt, alert_fxt),
    )


@pytest.fixture
def test_model_optional_json_provided(alert_fxt):
    return TestModelOptionalJson(
        alert=alert_fxt,
        alerts_list=[alert_fxt],
        alerts_dict={"alert1": alert_fxt},
        alerts_tuple=(alert_fxt, alert_fxt),
    )


@pytest.fixture
def test_model_optional_json_not_provided():
    return TestModelOptionalJson()


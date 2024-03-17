"""
pytest fixtures for sqlmodel
"""
import pytest
from sqlmodel import Session, SQLModel, StaticPool, create_engine


@pytest.fixture(scope='function')
def engine_fxt():
    """
    Create an in-memory sqlite engine

    :return: sqlite engine
    """
    return create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False}, poolclass=StaticPool)


@pytest.fixture(scope='session')
def session_fxt():
    """
    Create an in-memory sqlite session

    :return: sqlite session
    """
    # engine = engine_fxt
    engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

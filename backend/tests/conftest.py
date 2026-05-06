import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base

TEST_DB_URL = "sqlite:///./test.db"

@pytest.fixture(scope="session")
def test_db():
    engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestSession = sessionmaker(bind=engine)
    db = TestSession()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def mock_gemini_response():
    return [
        {
            "directive_text": "The Secretary, Revenue Department is directed to regularise the services within 30 days.",
            "responsible_designation": "Secretary, Revenue Department",
            "responsible_department": "Revenue Department",
            "action_type": "regularisation",
            "due_date_text": "within 30 days",
            "source_sentence": "The Secretary, Revenue Department is directed to regularise the services within 30 days.",
            "confidence": 0.95
        }
    ]

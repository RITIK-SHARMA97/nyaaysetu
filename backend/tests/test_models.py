from sqlalchemy.orm import configure_mappers

import app.models  # noqa: F401


def test_sqlalchemy_mappers_configure():
    configure_mappers()

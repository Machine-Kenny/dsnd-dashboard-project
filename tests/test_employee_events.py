import pytest
from pathlib import Path

project_root = Path(__file__).resolve().parent


@pytest.fixture
def db_path():
    return project_root / "employeess_events.db"


def test_db_exists(db_path):
    assert db_path.is_file(), "The SQLite database file does not exist."


@pytest.fixture
def db_conn(db_path):
    from sqlite3 import connect

    return connect(db_path)


@pytest.fixture
def table_names(db_conn):
    name_tuples = db_conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall()
    return [x[0] for x in name_tuples]


def test_employee_table_exists(table_names):
    assert (
        "employee" in table_names
    ), "The 'employee' table does not exist in the database."


def test_team_table_exists(table_names):
    error_message = "The 'team' table does not exist in the database."
    assert "team" in table_names, error_message


def test_employee_events_table_exists(table_names):
    assert (
        "employee_events" in table_names
    ), "The 'employee_events' table does not exist in the database."

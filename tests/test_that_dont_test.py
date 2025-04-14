import logging
from contextlib import contextmanager
from unittest.mock import patch

import pytest


class DatabaseConfig:
    @staticmethod
    def connection():
        return None


class SomeService:
    def do_action(self):
        try:
            with DatabaseConfig.connection() as conn:
                pass
        except ConnectionError as e:
            logging.error("Failed to connect to the database")
            # problem: does not forward message
            raise ConnectionError from e
            # solution a: call raise
            # raise
            # raise e
            # solution b :re-raise new error with the same message
            # raise ConnectionError(str(e)) from e


@pytest.fixture
def mock_service():
    return SomeService()


def test_that_dont_test_implementation_but_it_looks_like(mock_service, caplog):
    caplog.set_level(logging.ERROR)

    @contextmanager
    def fake_connection_error():
        raise ConnectionError("Connection failed")

    with pytest.raises(ConnectionError, match="Connection failed"):
        # Use the current module reference
        with patch.object(
                DatabaseConfig,
                "connection",
                # problem: fake_connection_error() called rise exception imminently
                # problem: no use of use_effect
                # problem: setup of behaviour insite of rises instead outside
                return_value=fake_connection_error(),
        ):
            mock_service.do_action()

            # problem: unreachable code due to exception being mock
            # problem: using logs for test assertions
            assert "Failed to connect to the database" in caplog.text


# def test_that_test_implementation(mock_service, caplog):
#     caplog.set_level(logging.ERROR)
#
#     with patch.object(
#             DatabaseConfig,
#             "connection",
#             side_effect=ConnectionError("Connection failed"),
#     ):
#         with pytest.raises(ConnectionError, match="Connection failed"):
#             # Use the current module reference
#             mock_service.do_action()
#
#
#     assert "Failed to connect to the database" in caplog.text

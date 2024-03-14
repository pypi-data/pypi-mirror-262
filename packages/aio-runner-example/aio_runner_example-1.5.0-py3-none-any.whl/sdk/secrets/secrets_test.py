import pytest
from vyper import v

from sdk.secrets.exceptions import NotFoundError
from sdk.secrets.secrets import Secrets


def test_get_secret_ok():
    v.set("DUMMY_SECRET_KEY", "value")

    secrets = Secrets()

    assert secrets.get_secret("DUMMY_SECRET_KEY") == "value"


def test_get_secret_lower_ok():
    v.set("DUMMY_SECRET_KEY", "value")

    secrets = Secrets()

    assert secrets.get_secret("dummy_secret_key") == "value"


def test_get_secret_not_found():
    v.set("DUMMY_SECRET_KEY", None)
    secrets = Secrets()

    with pytest.raises(NotFoundError):
        secrets.get_secret("DUMMY_SECRET_KEY")

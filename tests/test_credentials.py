import os
from unittest import mock

from pytest import raises

from limesurvey_manager.credentials.credentials import (
    MissingCredentialsError,
    set_creds,
)


@mock.patch.dict(os.environ, {"password": ""}, clear=True)
def test_cannot_have_empty_credentials():
    with raises(MissingCredentialsError):
        set_creds()

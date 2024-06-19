from json import load

import pytest
from limesurveyrc2api.limesurvey import LimeSurvey  # type:ignore

from limesurvey_manager.credentials.credentials import set_creds
from limesurvey_manager.manage import File


@pytest.fixture(scope="session")  # type:ignore
def setup_data():
    creds = set_creds()
    ls = LimeSurvey(creds.url, creds.username)
    yield creds, ls

    ls.close()


def test_can_login_to_limesurvey(setup_data):
    creds, ls = setup_data
    ls.open(creds.password)
    assert ls.session_key

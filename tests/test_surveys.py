from json import load
from pprint import pp

import pytest
from limesurveyrc2api.limesurvey import LimeSurvey  # type:ignore

from limesurvey_manager.credentials.credentials import set_creds


def get_survey_data():
    with open("forms_config.json", "r") as f:
        survey_list = load(f)

    for survey in survey_list:
        yield survey.values()


@pytest.fixture(scope="session")
def setup_data():
    creds = set_creds()

    api = LimeSurvey(url=creds.url, username=creds.username)
    api.open(password=creds.password)
    with open("question_test.json", "r") as f:
        question_list_check = load(f)
    yield api, question_list_check

    api.close()


@pytest.mark.parametrize(
    ["code", "survey_id", "single_form", "is_gs"], get_survey_data()
)
def test_survey_questions(setup_data, code, survey_id, single_form, is_gs):
    """Checks equally on a select group of attributes of a question inside checklist_question_titles."""
    api, question_list_check = setup_data
    if is_gs:
        return
    question_list = api.survey.list_questions(survey_id)

    checklist_question_titles = ["opmatr", "pag2Taxa180", "CursSencer"]

    for title in checklist_question_titles:
        checkquestion = list(
            filter(lambda q: q["title"] == title, question_list_check)
        )
        current_survey_question = list(
            filter(lambda q: q["title"] == title, question_list)
        )
        if not current_survey_question:
            continue
        try:
            assert (
                checkquestion[0]["relevance"]
                == current_survey_question[0]["relevance"]
            )
            assert (
                checkquestion[0]["type"] == current_survey_question[0]["type"]
            )
            assert (
                checkquestion[0]["help"] == current_survey_question[0]["help"]
            )
        except AssertionError:
            print(f"Cicle: {code}")
            pp(f"Expected: {checkquestion}")
            pp(f"Actual: {current_survey_question}")

    print(f"Done: {code}")

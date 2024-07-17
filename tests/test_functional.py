from json import load
from unittest import mock

import pytest

from limesurvey_manager.manage import File, select_option


def test_store_data_in_json():
    data = [{"survey_id": 123456}]

    file = File(data)

    file.save_as_json()

    with open(file.file_path, "r") as f:
        json_contents = load(f)

    assert json_contents == data
    file.remove()


@mock.patch("limesurvey_manager.manage.menu")
@pytest.mark.parametrize(
    "option,function",
    [
        (
            "files",
            "limesurvey_manager.manage.export_files.export_participant_files",
        ),
        ("invitations", "limesurvey_manager.manage.main.invite_participants"),
    ],
)
def test_check_correct_function_called_in_manage(menu_mock, option, function):
    menu_mock.selection = option

    with mock.patch(function) as export_files_mock:
        select_option(menu_mock)
        export_files_mock.assert_called_once()

"""Manage Limesurvey petitions."""

from limesurveyrc2api.limesurvey import LimeSurvey
from limesurveyrc2api.exceptions import LimeSurveyError
from collections import OrderedDict
import config as cfg
import base64

from exceptions import ParticipantError


class LSCon(LimeSurvey):
    def __init__(self, url, username):
        """Initialize class."""
        super().__init__(url, username)

    def get_participant_by_token(self, surveyid, token):
        """Fetch participant data from a survey."""
        try:
            return self.token.get_participant_properties(
                surveyid, token_query_properties={"token": token})
        except LimeSurveyError as e:
            return ParticipantError("Aquest token no existeix.")

    def get_all_participant_files(self, surveyid: str, token: str):
        """Get all files imported by a participant based on her token and returns the data for further processing."""

        cicle_files = []
        general_files = []
        def ensure_dictionary(suspect):
            check = isinstance(suspect, dict)
            if not check:
                return {}
            return suspect

        # # Participant token to search for.
        # al_data = self.get_participant_by_token(cfg.GENERAL_FORM_ID, token)

        # al_fullname = f"{al_data['lastname']}, {al_data['firstname']}"
        # al_cicle = al_data["attribute_3"]
        # if len(al_cicle) > 3:
        #     al_cicle = al_cicle[3]

        # # Create alumnus folder
        # al_path = f"{exported_path}/{al_cicle}/{al_fullname}"

        params = OrderedDict([
            ("sessionkey", self.session_key),
            ("surveyid", surveyid),
            ("token", token)
        ])

        # Get a list of all the files related to that participant
        cicle_response = self.query("get_uploaded_files", params)
        if cicle_response:
            cicle_files = [file for file in cicle_response.values()]

        # TODO: Extract files form the general form.
        params["surveyid"] = cfg.GENERAL_FORM_ID
        general_response = self.query("get_uploaded_files", params)
        if general_response:
            general_files = [file for file in general_response.values()]

        return [*cicle_files, *general_files]

        for [key, value] in results.items():
            # Check if table exists
            if key == "status":
                print("La taula de participants no existeix.")
                continue

            # Decode file
            with open(f"{al_path}/{al_fullname} - {value['meta']['question']['title']}.pdf", "wb") as f:
                f.write(base64.b64decode(value["content"]))

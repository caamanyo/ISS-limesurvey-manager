"""Convert form data to dictionary to send to LS API."""

from dataclasses import dataclass, fields


@dataclass
class SearchConditions:
    firstname: str = None
    lastname: str = None
    sent: list = None
    completed: str = None

    def _dropdown_options(self, opt: int):
        match opt:
            case 0:
                return None
            case 1:
                return ["<>", "N"]
            case 2:
                return ["=", "N"]

    def _text_input(self, value: str):
        return ["LIKE", value]

    def set_inv_sent(self, value: int, date: str = None):
        self.sent = self._dropdown_options(value)

    def set_lastname(self, value: str):
        self.lastname = self._text_input(value)

    def set_firstname(self, value: str):
        self.firstname = self._text_input(value)

    def set_complete(self, value: int):
        self.completed = self._dropdown_options(value)

    def to_dict(self):
        condition_dict = {}
        for field in fields(self):
            val = getattr(self, field.name)
            if val is not None:
                condition_dict[field.name] = val

        return condition_dict

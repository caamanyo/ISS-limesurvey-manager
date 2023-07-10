"""Convert form data to dictionary to send to LS API."""

from dataclasses import dataclass, fields


@dataclass
class SearchConditions:
    lastname: str = None
    sent: list = None

    def set_inv_sent(self, data: int, date: str = None):
        match data:
            case 1:
                self.sent = ["<>", "N"]
            case 2:
                self.sent = ["=", "N"]

    def set_lastname(self, value: str):
        self.lastname = ["LIKE", value]

    def to_dict(self):
        condition_dict = {}
        for field in fields(self):
            val = getattr(self, field.name)
            if val is not None:
                condition_dict[field.name] = val

        print(condition_dict)
        return condition_dict

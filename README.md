# Enrollment manager for Limesurvey
This is an ad hoc GUI to administer a school's enrollment process. It requires a functioning Limesurvey server with remote control activated (See [](https://manual.limesurvey.org/RemoteControl)).

# Dependencies
- PyQt6
- Limesurveyrc2api = 2.0.0

# Usage
Create a `.env` file inside the root folder with the variables:
- url: the Limesurvey remote control address.
- ls_user: Limesurvey username.
- password: Limesurvey password.
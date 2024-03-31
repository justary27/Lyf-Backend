import json
from firebase_admin import initialize_app, credentials
from pyrebase import initialize_app as initialize_pyrebase
from globals import variables


def initialize_firebase_services() -> None:
    with open("web_api_creds.json") as f:
        app_creds = json.load(f)
        variables.firebase_instance = initialize_pyrebase(app_creds)

        initialize_app(
            credentials.Certificate(
                "service_account_creds.json"
            )
        )

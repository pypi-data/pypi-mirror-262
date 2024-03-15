"""OneDrive class."""
from t_office_365.endpoints import OnedriveEndpoints


class Onedrive:
    """OneDrive class."""

    def __init__(self, account):
        self.endpoints = OnedriveEndpoints(account)

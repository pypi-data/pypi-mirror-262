"""Excel class."""
from t_office_365.endpoints import ExcelEndpoints


class Excel:
    """Excel class."""

    def __init__(self, account):
        self.endpoints = ExcelEndpoints(account)

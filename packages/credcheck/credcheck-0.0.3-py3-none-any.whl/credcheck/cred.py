import requests


class Credential:
    def __init__(self, username, password, doi):
        self.username = username
        self.password = password
        self.doi = doi

    def __str__(self):
        return f"username: {self.username}, password: {self.password}"

    def is_authenticated(self):
        """
        Test whether a user is authenticated
        :return: True if authenticated, False if not
        """
        data = {"usr": self.username, "pwd": self.password}

        response = requests.post(
            f"https://doi.crossref.org/servlet/login",
            data=data,
        )

        return (
            response.json()["success"] != "false"
            and response.json()["success"] is not False
        )

    def is_authorised(self):
        """
        Test whether a user is authorised
        :return: True if authorised, False if not
        """
        url = "https://doi.crossref.org/servlet/reports"
        params = {
            "login_id": self.username,
            "login_passwd": self.password,
            "doi": self.doi,
            "action": "doiHistoryReport",
            "page": 0,
            "show": "Show",
        }

        response = requests.get(url, params=params)

        return not (
            "Not allowed to access prefix" in response.text
            or "DOI not found" in response.text
            or "Welcome to Crossref" in response.text
        )

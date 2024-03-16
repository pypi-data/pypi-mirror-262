class KopeechkaApiError(Exception):
    def __init__(self, status: str, value: str):
        self.status = status
        self.value = value

    def __str__(self):
        return self.value


class TimeOut(Exception):
    def __str__(self):
        return "Timed out"


def catch_error(data: dict):
    if data.get("status") == "ERROR":
        raise KopeechkaApiError(data.get("status"), data.get("value"))

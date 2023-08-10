import datetime


class ResponseData:

    def __init__(self, status_code: int, content: dict):
        self.status_code = status_code
        self.time = datetime.datetime.now()
        self.content = content
    
    def get_data(self):
        return {
            "status_code": self.status_code,
            "time": self.time.isoformat(),
            "content": self.content
        }

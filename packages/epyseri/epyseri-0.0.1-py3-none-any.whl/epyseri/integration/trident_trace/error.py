class ServiceError(Exception):
    pass

class TridentTraceAPIError(Exception):
    def __init__(self, message, api_response=None, http_status_code=None, raw_http_client=None):
        self.message = message
        self.api_response = api_response
        self.http_status_code = http_status_code
        self.raw_http_client = raw_http_client

    def str(self):
        return self.message
    
class ErrorHandler:
    pass
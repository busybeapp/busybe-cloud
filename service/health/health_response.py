class HealthResponse(object):

    def __init__(self):
        self.status = 'OK'
        self.message = 'Service is up and running'

    def to_client(self):
        return {'status': self.status, 'message': self.message}

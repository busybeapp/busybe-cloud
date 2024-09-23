import uuid


class IdManager(object):

    @staticmethod
    def assign():
        return str(uuid.uuid4())
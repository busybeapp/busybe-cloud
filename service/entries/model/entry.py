

class Entry(object):

    def __init__(self, id, title):
        self.id = id
        self.title = title

    @staticmethod
    def from_json(json_data):
        _id = json_data.get('id')
        _title = json_data.get('title')

        if not _title:
            raise ValueError("Invalid entry: 'title' are required")

        return Entry(_id, _title)

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title
        }
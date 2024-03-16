from komoutils.db.mongodb_reader_writer import MongoDBReaderWriter


class Crud(MongoDBReaderWriter):
    def __init__(self, uri: str, db_name: str):
        super().__init__(uri, db_name)

    def read_symbol_data(self, filters=None):
        if filters is None:
            filters = {}
        return self.read(filters)

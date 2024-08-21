

from firebase_admin import initialize_app, get_app, \
    credentials, firestore


class FirestoreHandler:
    def __init__(self):
        self.cred = credentials.Certificate('service-account.json')

    def get_colletion(self, collection: str):
        db = self.__get_db()
        return db.collection(collection)

    def __init_app(self):
        try:
            app = get_app()
        except ValueError:
            app = initialize_app(self.cred)
        return app

    def __get_db(self):
        return firestore.client(self.__init_app())

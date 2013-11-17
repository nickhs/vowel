from createdb import run as init_db
from app import user_datastore, db


def run():
    init_db()
    user_datastore.create_user(email='test@vowel.io', password='test')
    db.session.commit()

if __name__ == '__main__':
    run()

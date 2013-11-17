from app import db


def run():
    print "WARNING: This is a destructive action"

    db.drop_all()
    db.create_all()

if __name__ == '__main__':
    run()

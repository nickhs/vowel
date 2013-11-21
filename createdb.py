from app import db
from models import *


def run():
    print "WARNING: This is a destructive action"

    db.drop_all()
    db.create_all()

if __name__ == '__main__':
    run()

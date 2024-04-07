from DataBase.DB import db
import datetime


class DB_Links(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    old_url = db.Column(db.String, nullable=False)
    shorten_url = db.Column(db.String, nullable=False, unique=True)
    expire_date = db.Column(db.DateTime, nullable=False)

    @staticmethod
    def create_new_link(old_url, shorten_url, expire_date):
        new_url = DB_Links(old_url=old_url, shorten_url=shorten_url, expire_date=expire_date)
        db.session.add(new_url)
        db.session.commit()

    @staticmethod
    def find_object_link(shorten_url):
        entry_object = DB_Links.query.filter_by(shorten_url=shorten_url).first()
        return entry_object

    @staticmethod
    def delete_object_link(shorten_url):
        entry_object = DB_Links.query.filter_by(shorten_url=shorten_url).first()
        entry_object.delete()
        db.session.commit()


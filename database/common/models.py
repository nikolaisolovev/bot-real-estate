from datetime import datetime

import peewee as pw

db = pw.SqliteDatabase('real_estate.db')


class ModelBase(pw.Model):
    created_at = pw.DateField(default=datetime.now)

    class Meta:
        database = db


class History(ModelBase):
    city = pw.TextField()
    county = pw.TextField()
    price = pw.IntegerField()
    address = pw.TextField()
    user_id = pw.TextField()
    photo = pw.TextField()
    url = pw.TextField()
    
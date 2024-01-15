from flask import *
from peewee import *

app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_object(__name__)
db = PostgresqlDatabase(user='postgres',
                        password='9502588011',
                        host='localhost',
                        port='5432',
                        database='family_book')


class BaseModel(Model):
    class Meta:
        database = db

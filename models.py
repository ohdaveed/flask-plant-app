import date

from peewee import *

DATABASE = SqliteDatabase('plants.sqlite')

class Plant(Model):
	name = CharField()
	scientific_name = Charfield()
	order = Charfield()
	image = Charfield()
	created_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Plant], safe=True)
	print("Tables Created")
	DATABASE.close()
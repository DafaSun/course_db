from config import *
from peewee import *


class FCS(BaseModel):
    surname = CharField(max_length=50, null=True)
    maiden_surname = CharField(max_length=50, null=True)
    name = CharField(max_length=50, null=True)
    patronymic = CharField(max_length=50, null=True)


FCS.create_table()


class Gender(BaseModel):
    gender_name = CharField(max_length=50, unique=True, null=False)


Gender.create_table()


class Person(BaseModel):
    fcs = ForeignKeyField(FCS, backref='person', null=False)
    birthday = DateField(null=True)
    day_of_die = DateField(null=True)
    gender = ForeignKeyField(Gender, backref='person', null=False)


Person.create_table()


class ContactData(BaseModel):
    person = ForeignKeyField(Person, backref='contact', null=False)
    phone_number = CharField(max_length=50, null=True)
    email = CharField(max_length=50, null=True)


ContactData.create_table()


class EducationLevel(BaseModel):
    level_name = CharField(max_length=50, unique=True, null=False)


EducationLevel.create_table()


class TimeInterval(BaseModel):
    begin_time = DateTimeField(null=True)
    end_time = DateTimeField(null=True)


TimeInterval.create_table()


class Address(BaseModel):
    country = CharField(max_length=50, null=False)
    region = CharField(max_length=50, null=True)
    city = CharField(max_length=50, null=True)
    street = CharField(max_length=50, null=True)
    house = IntegerField(null=True)
    flat = IntegerField(null=True)


Address.create_table()


class Organisation(BaseModel):
    organisation_name = CharField(max_length=50, null=True)
    address = ForeignKeyField(Address, backref='organisation', null=True)


Organisation.create_table()


class Education(BaseModel):
    person_id = ForeignKeyField(Person, backref='education', null=True)
    profession = CharField(max_length=50, null=True)
    education_organisation = ForeignKeyField(Organisation, backref='education', null=True)
    level = ForeignKeyField(EducationLevel, backref='education', null=True)
    time = ForeignKeyField(TimeInterval, backref='education', null=True)


Education.create_table()


class Work(BaseModel):
    person_id = ForeignKeyField(Person, backref='work', null=False)
    post = CharField(max_length=50, null=True)
    organisation = ForeignKeyField(Organisation, backref='work', null=True)
    time = ForeignKeyField(TimeInterval, backref='work', null=True)


Work.create_table()


class Residence(BaseModel):
    person_id = ForeignKeyField(Person, backref='residence', null=False)
    address = ForeignKeyField(Address, backref='residence', null=False)
    time = ForeignKeyField(TimeInterval, backref='residence', null=True)


Residence.create_table()


class Marriage(BaseModel):
    wife = ForeignKeyField(Person, backref='marriage_wife', null=False)
    husband = ForeignKeyField(Person, backref='marriage_husband', null=False)
    time = ForeignKeyField(TimeInterval, backref='marriage', null=True)


Marriage.create_table()


class Children(BaseModel):
    parent_id = ForeignKeyField(Person, backref='children_parent', null=False)
    child_id = ForeignKeyField(Person, backref='children_child', null=False)


Children.create_table()


class User(BaseModel):
    login = CharField(max_length=50, unique=True, null=False)
    password = CharField(max_length=50, unique=True, null=False)


User.create_table()


class Story(BaseModel):
    user = ForeignKeyField(User, backref='story', null=False)
    story = TextField()
    person = ForeignKeyField(Person, backref='story', null=True)
    date = DateField(null=True)


Story.create_table()

class Belonging_to_user(BaseModel):
    user_id = ForeignKeyField(User, backref='belonging_to_user_user', null=False)
    person_id = ForeignKeyField(Person, backref='belonging_to_user_person', null=False)


Belonging_to_user.create_table()

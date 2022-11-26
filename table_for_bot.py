from peewee import (
    Model,
    SqliteDatabase,
    CharField,
    IntegerField,
    ForeignKeyField,
)

db = SqliteDatabase('message_client.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_name = CharField(max_length=50)
    chat_id = IntegerField()


class Message(BaseModel):
    message = CharField(max_length=500)
    chat_id = ForeignKeyField(User)


if __name__ == '__main__':
    db.create_tables([Message, User])

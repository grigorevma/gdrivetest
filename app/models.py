from tortoise.models import Model
from tortoise import fields


class Users(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    password = fields.BinaryField()
    events: fields.ReverseRelation["Files"]
    archive: fields.ReverseRelation["Archiv"]

    def __str__(self):
        return self.name


class Files(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()

    userid: fields.ForeignKeyRelation[Users] = fields.ForeignKeyField(
        "models.Users", related_name="events"
    )

    def __str__(self):
        return self.name


class Archiv(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()

    userid: fields.ForeignKeyRelation[Users] = fields.ForeignKeyField(
        "models.Users", related_name="archive"
    )

    def __str__(self):
        return self.name

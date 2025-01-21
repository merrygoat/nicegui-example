# This is where the databases tables and fields are defined.

# Where a foreign key is exposed on the parent object as a backref, I have added an annotated class object on the
# parent. This is not technically necessary but helps the IDE, as otherwise it marks backrefs as unknown when they are
# referenced.

import peewee

# Pragmas ensures foreign key constraints are enabled - they are disabled by default in SQLite.
db = peewee.SqliteDatabase('data.db', pragmas={'foreign_keys': 1})


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Party(BaseModel):
    id = peewee.AutoField()
    name = peewee.CharField(null=True)
    candidates: "Candidate"  # backref


class Candidate(BaseModel):
    id = peewee.AutoField()
    first_name = peewee.CharField()
    last_name = peewee.CharField()
    email = peewee.CharField()
    party = peewee.ForeignKeyField(Party, backref='candidates', null=True)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


db.create_tables([Candidate, Party])

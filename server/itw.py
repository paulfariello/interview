#
# Copyright (c) 2017 Paul Fariello <paul@fariello.eu>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import peewee
from peewee import PrimaryKeyField, IntegerField, CharField, UUIDField, ForeignKeyField, DateTimeField, datetime
import playhouse.db_url
from urllib.parse import urlparse

import uniqid

DB = peewee.Proxy()

def atomic(f):
    def wrapper(*args):
        with DB.atomic():
            return f(*args)
    return wrapper

def connect(url):
    """Connect Interview to the database

    :param url: the database scheme
    :type url: str
    """
    args = {}
    parsed = urlparse(url)
    if 'sqlite' in parsed.scheme:
        args['pragmas'] = (('foreign_keys', 'ON'),)
    DB.initialize(playhouse.db_url.connect(url, **args))


def create_tables():
    """Create required table if necessary"""
    DB.create_tables([Applicant, Interview, Exercice, Tag, ExerciceTagRel, ExerciceAttribution, Answer])


class JSONObject():
    """JSON object that can be dumped into raw json"""
    @property
    def json(self):
        """simple representation of the object that can feed json.dumps"""
        raise NotImplementedError


class ItwModel(peewee.Model):
    """Base class for all Interview model classes"""
    class Meta:
        database = DB


class Applicant(ItwModel, JSONObject):
    """Applicant"""
    _id = PrimaryKeyField()
    uid = UUIDField()
    name = CharField()

    @property
    def json(self):
        return {"uid": uniqid.encode(self.uid),
                "name": self.name}


class Interview(ItwModel, JSONObject):
    """Interview"""
    _id = PrimaryKeyField()
    uid = UUIDField()
    token = UUIDField()
    start_date = DateTimeField(null=True)
    end_date = DateTimeField(null=True)
    applicant = ForeignKeyField(Applicant, related_name="interviews")

    @property
    def json(self):
        return {"uid": uniqid.encode(self.uid),
                "token": uniqid.encode(self.token),
                "applicant": uniqid.encode(self.applicant.uid),
                "start_date": self.start_date,
                "end_date": self.end_date,
                "exercices": [uniqid.encode(answer.exercice.uid)
                              for answer in sorted(self.exercices, key=lambda e: e.index)]}


class Exercice(ItwModel, JSONObject):
    """Exercice"""
    _id = PrimaryKeyField()
    uid = UUIDField()
    question = CharField()

    @property
    def json(self):
        return {"uid": uniqid.encode(self.uid),
                "question": self.question,
                "tags": [rel.tag.json for rel in self.tags]}


class Tag(ItwModel, JSONObject):
    """Tag for exercices"""
    _id = PrimaryKeyField()
    name = CharField()

    @property
    def json(self):
        return self.name


class ExerciceTagRel(ItwModel):
    """Exercice tag many-to-many relationship"""
    _id = PrimaryKeyField()
    tag = ForeignKeyField(Tag, related_name='exercices')
    exercice = ForeignKeyField(Exercice, related_name='tags')

class ExerciceAttribution(ItwModel):
    """Exercice Interview many-to-many relationship also linking to answers"""
    _id = PrimaryKeyField()
    interview = ForeignKeyField(Interview, related_name='exercices')
    exercice = ForeignKeyField(Exercice)
    index = IntegerField()

    class Meta:
        indexes = ((('interview', 'exercice'), True),
                   (('interview', 'index'), True))

    @property
    def json(self):
        return {"interview": uniqid.encode(self.interview.uid),
                "uid": uniqid.encode(self.exercice.uid),
                "question": self.exercice.question,
                "tags": [rel.tag.json for rel in self.exercice.tags],
                "index": self.index}

class Answer(ItwModel):
    """Exercice answer"""
    _id = PrimaryKeyField()
    exercice = ForeignKeyField(ExerciceAttribution, related_name='answers')
    answer = CharField(null=True)
    date = DateTimeField(default=datetime.datetime.now)

    @property
    def json(self):
        return {"answer": self.answer,
                "date": self.date.isoformat()}

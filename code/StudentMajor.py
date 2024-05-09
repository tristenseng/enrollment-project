import mongoengine
from mongoengine import *
from Major import Major
import datetime

class StudentMajor(EmbeddedDocument):
    """"""
    # The  parent order that this is a member of.
    #section = ReferenceField(Section, required=True, reverse_delete_rule=mongoengine.DENY)
    # This will be replaced by a reference to an instance of the Product class.
    #student = ReferenceField(Student, required=True)
    declarationDate = DateTimeField(db_field='declaration_date', required=True)
    major = EmbeddedDocumentField(Major, db_field='major', required=True)


    def __init__(self, declarationDate: datetime, major: major, *args, **values):
        """
        """
        super().__init__(*args, **values)
        self.declarationDate = declarationDate
        self.major = major


    def __str__(self):
        return f'Student Major: {self.major}, Declaration date:{self.declarationDate}'


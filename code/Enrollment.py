import mongoengine
from mongoengine import *
from LetterGrade import LetterGrade
from PassFail import PassFail


class Enrollment(EmbeddedDocument):
    """An individual product that is part of an order.  This could easily be done
    using a one to few, in which case it would be just an element in an array
    within the Order class, but I wanted to use this as a demonstration of how to
    do the same thing using a bidirectional relationship."""
    # The  parent order that this is a member of.
    #section = ReferenceField(Section, required=True, reverse_delete_rule=mongoengine.DENY)
    # This will be replaced by a reference to an instance of the Product class.
    #student = ReferenceField(Student, required=True)
    passFail = EmbeddedDocumentListField(PassFail, db_field='pass_fail')
    letterGrade = EmbeddedDocumentListField(LetterGrade, db_field='letter_grade')

    def __init__(self, passFail: PassFail, letterGrade: LetterGrade, *args, **values):
        """
        """
        super().__init__(*args, **values)
        self.passFail = passFail
        self.letterGrade = letterGrade


    def __str__(self):
        return f'Enrollment: {self.passFail}{self.letterGrade}'


from mongoengine import *
import datetime


class LetterGrade(EmbeddedDocument):
    """

    """
    grades = ('A', 'B', 'C')
    minSatisfactory = StringField(db_field='min_satisfactory', choices='grades', required=True)

    def __init__(self, minSatisfactory: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.minSatisfactory = minSatisfactory

    def __str__(self):
        return f'Min Satisfactory grade for Enrollment: {self.minSatisfactory}'

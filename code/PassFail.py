from mongoengine import *
import datetime


class PassFail(EmbeddedDocument):
    """

    """
    applicationDate = DateTimeField(db_field='application_date', required=True)

    def __init__(self, applicationDate: datetime, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.applicationDate = applicationDate

    def __str__(self):
        return f'Enrollment date to Pass/Fail: {self.applicationDate}'

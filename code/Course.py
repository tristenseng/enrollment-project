from mongoengine import *
from Department import Department
from datetime import datetime
from decimal import *

class Course(Document):
    """."""

    courseNumber = IntField(db_field='course_number', min_length=100, max_length=700, required=True)
    courseName = StringField(db_field='course_name', required=True)
    description = StringField(db_field='description', required=True)
    units = IntField(db_field='units', min_length=1, max_length=6, required=True)

    sections = ListField(ReferenceField('Section'))

    department = ReferenceField('Department')

    meta = {'collection': 'courses',
            'indexes': [
                {'unique': True, 'fields': ['Department.departmentAbbreviation'], 'name': 'courses_uk_01'},
                {'unique': True, 'fields': ['chairName'], 'name': 'courses_uk_02'}
            ]}

    def __init__(self, courseNumber: int, courseName: str, description: str, units: int,
                 department: Department, *args, **values):
        """
        Create a new instance of a Course object

        :param name:           The name of a unique product item.

        """
        super().__init__(*args, **values)
        self.department = department
        if self.sections is None:
            self.sections = []  # initialize to no sections in the department yet
        self.courseNumber = courseNumber
        self.courseName = courseName
        self.description = description
        self.units = units

    def __str__(self):
        """
        Returns a string representation of the Department instance.
        :return: A string representation of the Department instance.
        """
        results = (f'Course number: {self.courseNumber}, Course name: {self.courseName}, Department: {self.department}'
                   f'Description: {self.description}, Units:{self.units}')

        return results


    def add_section(self,section):
        """
        \
        :param item:    An instance of OrderItem class to be added to this .
        If this Product is already in the order, this call is ignored.
        :return:    None
        """
        for existing_section in self.sections:
            if section.equals(existing_section):
                return  # Already in the dept, don't add it.
        self.sections.append(section)

    def remove_section(self, section):
        """
        Removes a section from the course.

        :return:        None
        """
        for existing_section in self.sections:
            # Check to see whether this next order item is the one that they want to delete
            if section.equals(existing_section):
                # They matched on the Product, so they match.  For the remove_item use
                # case, it doesn't really matter what quantity is called for.  I only used
                # an instance of OrderItem here to be consistent with add_item.
                self.sections.remove(existing_section)
                # At this point, the OrderItem object should be deleted since there is
                # no longer a reference to it from Order.
                existing_section.delete()
                return
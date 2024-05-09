from mongoengine import *
from Enrollment import Enrollment
from Course import Course
from datetime import datetime
from decimal import *

class Section(Document):
    """."""
    semesters = ('Fall', 'Spring', 'Summer I', 'Summer II', 'Summer III', 'Winter')
    buildings = ('ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC')
    schedules = ('MW', 'TuTh', 'MWF', 'F', 'S')

    sectionNumber = IntField(db_field='section_number', required=True)
    semester = EnumField(db_field='semester', choices='semesters', required=True)
    sectionYear = IntField(db_field='section_number', required=True)
    building = EnumField(db_field='building', choices='buildings', required=True)
    room = IntField(db_field='section_number', required=True)
    instructor = StringField(db_field='instructor', required=True)
    schedule = EnumField(db_field='schedule', choices='schedules', required=True)
    startTime = DateTimeField(db_field='start_time', required=True)

    enrollments = EmbeddedDocumentListField('Enrollment')

    course = ReferenceField('Course')

    meta = {'collection': 'sections',
            'indexes': [
                {'unique': True, 'fields': ['Course', 'section_number', 'semester', 'section_year'],
                 'name': 'sections_uk_01'},
                {'unique': True, 'fields': ['semester', 'section_year', 'building', 'room', 'schedule', 'start_time'],
                 'name': 'sections_uk_02'},
                {'unique': True, 'fields': ['semester', 'section_year', 'schedule', 'start_time', 'instructor'],
                 'name': 'sections_uk_03'},
                {'unique': True, 'fields': ['semester', 'section_year', 'Course.department_abbreviation',
                                            'Course.course_number', 'Student.student_id'], 'name': 'sections_uk_05'},
            ]}


    def __init__(self, course: Course, sectionNumber: int, semester: semesters, sectionYear: int, building: buildings, room: int,
                 instructor: str, schedule: schedules, *args, **values):
        """
        Create a new instance of a Section object

        :param name:           The name of a unique section.

        """
        super().__init__(*args, **values)
        self.course = course
        self.sectionNumber = sectionNumber
        self.semester = semester
        self.sectionYear = sectionYear
        self.building = building
        self.room = room
        self.instructor = instructor
        self.schedule = schedule

    def __str__(self):
        """
        Returns a string representation of the Section instance.
        :return: A string representation of the Section instance.
        """
        results = (f'Course: {self.course}, Section number: {self.sectionNumber}, Semester: {self.semester}'
                   f'Section year: {self.sectionYear}, Building:{self.building}, Room: {self.room},'
                   f'Instructor: {self.instructor}, Schedule: {self.schedule}')

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
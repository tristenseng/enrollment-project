from mongoengine import *
from datetime import datetime
from decimal import *
class Department(Document):
    """An item available for purchase from the enterprise to a single customer for an agreed upon price."""
    buildings = ('ANAC', 'CDC', 'DC', 'ECS', 'EN2', 'EN3', 'EN4', 'EN5', 'ET', 'HSCI', 'NUR', 'VEC')

    name = StringField(db_field='name', max_length=50, required=True)
    abbreviation = StringField(db_field='_id', max_length=6, required=True)
    chairName = StringField(db_field='chair_name', max_length=80, required=True)
    building = EnumField(db_field='building', choices='buildings', required=True)
    office = IntField(db_field='office', required=True)
    description = StringField(db_field='description', max_length=800, required=True)

    courses = ListField(ReferenceField('Course'))

    majors = ListField(ReferenceField('Major'))

    meta = {'collection': 'departments',
            'indexes': [
                {'unique': True, 'fields': ['abbreviation'], 'name': 'departments_uk_01'},
                {'unique': True, 'fields': ['chairName'], 'name': 'departments_uk_02'},
                {'unique': True, 'fields': ['building', 'office'], 'name': 'departments_uk_03'},
                {'unique': True, 'fields': ['name'], 'name': 'departments_uk_04'}
            ]}

    def __init__(self,  name: str, abbreviation: str, chairName: str, building: buildings,
                 office: int, description: str, *args, **values):
        """
        Create a new instance of an Department object

        :param name:           The name of a unique product item.

        """
        super().__init__(*args, **values)
        if self.courses is None:
            self.courses = []  # initialize to no courses in the department yet
        if self.majors is None:
            self.majors = []  # initialize to no majors in the department yet.
        self.name = name
        self.abbreviation = abbreviation
        self.chairName = chairName
        self.building = building
        self.office = office
        self.description = description

    def __str__(self):
        """
        Returns a string representation of the Department instance.
        :return: A string representation of the Department instance.
        """
        results = (f'Department: {self.name}, {self.abbreviation}, Chair name: {self.chairName}, Building: {self.building},'
                   f'Office: {self.office}, Description: {self.description}')

        return results

    def add_course(self,course):
        """
        Adds an item to the Product.
        :param item:    An instance of OrderItem class to be added to this Product.
        If this Product is already in the order, this call is ignored.
        :return:    None
        """
        for existing_course in self.courses:
            if course.equals(existing_course):
                return  # Already in the dept, don't add it.
        self.courses.append(course)

    def remove_course(self, course):
        """
        Removes a course from the department.

        :return:        None
        """
        for existing_course in self.courses:
            # Check to see whether this next order item is the one that they want to delete
            if course.equals(existing_course):
                # They matched on the Product, so they match.  For the remove_item use
                # case, it doesn't really matter what quantity is called for.  I only used
                # an instance of OrderItem here to be consistent with add_item.
                self.courses.remove(existing_course)
                # At this point, the OrderItem object should be deleted since there is
                # no longer a reference to it from Order.
                existing_course.delete()
                return
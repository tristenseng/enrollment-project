
from mongoengine import *
from datetime import datetime
from StudentMajor import StudentMajor


class Student(Document):
    """"""
    studentId = IntField(db_field='_id', required=True)
    last_name = StringField(db_field='last_name', required=True)
    first_name = StringField(db_field='first_name', required=True)
    email = StringField(db_field='email', required=True)

    studentMajors = EmbeddedDocumentListField('StudentMajor')

    meta = {'collection': 'students',
            'indexes': [
                {'unique': True, 'fields': ['_id'], 'name': '_id'},
                {'unique': True, 'fields': ['last_name', 'first_name'], 'name': 'students_uk_01'},
                {'unique': True, 'fields': ['email'], 'name': 'students_uk_02'}
            ]}

    def __init__(self, studentId: int, lastName: str, firstName: str, email: str, *args, **values):
        """

        """
        super().__init__(*args, **values)
        if self.studentMajors is None:
            self.studentMajors = []  # initialize to no majors in studentmajors, yet.
        self.studentId = studentId
        self.lastName = lastName
        self.firstName = firstName
        self.email = email


    def __str__(self):
        """
        Returns a string representation of the Order instance.
        :return: A string representation of the Order instance.
        """
        results = f'Student name: {self.lastName},{self.firstName}, Email: {self.email}.'
        for studentMajor in self.studentMajors:
            results = results + '\n\t' + f'Item: {studentMajor.major}'
        return results
    '''
    def add_item(self, item):
        """
        Adds an item to the Order.  Note that the item argument is an instance of the
        OrderItem class, and as such has both the product that is ordered and
        the quantity.  We cannot have more than one OrderItem for any Order for the
        same product.
        :param item:    An instance of OrderItem class to be added to this Order.  If
        an OrderItem    this Product is already in the order, this call is ignored.
        :return:    None
        """
        for already_ordered_item in self.orderItems:
            if item.equals(already_ordered_item):
                return  # Already in the order, don't add it.
        self.orderItems.append(item)
        # There is no need to update the OrderItem to point to this Order because the
        # constructor for OrderItem requires an Order and that constructor calls this
        # method.  Of course, the liability here is that someone could create an instance
        # of OrderItem withOUT using our constructor.  Argh.

    def remove_item(self, item):
        """
        Removes a Product from the order.  Note that the item argument is an instance of the
        OrderItem class, but we ignore the quantity.
        :param item:    An instance of the OrderItem class that includes the Product that
                        we are removing from the order.  If this Product is not already in
                        the order, the call is ignored.
        :return:        None
        """
        for already_ordered_item in self.orderItems:
            # Check to see whether this next order item is the one that they want to delete
            if item.equals(already_ordered_item):
                # They matched on the Product, so they match.  For the remove_item use
                # case, it doesn't really matter what quantity is called for.  I only used
                # an instance of OrderItem here to be consistent with add_item.
                self.orderItems.remove(already_ordered_item)
                # At this point, the OrderItem object should be deleted since there is
                # no longer a reference to it from Order.
                already_ordered_item.delete()
                return'''

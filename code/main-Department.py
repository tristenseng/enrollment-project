import pymongo
from pymongo import MongoClient
from pprint import pprint
import getpass
from menu_definitions import menu_main
from menu_definitions import add_menu
from menu_definitions import delete_menu
from menu_definitions import list_menu
from datetime import time, datetime


def add(db):
    """
    Present the add menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    add_action: str = ''
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
        exec(add_action)


def delete(db):
    """
    Present the delete menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    delete_action: str = ''
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
        exec(delete_action)


def list_objects(db):
    """
    Present the list menu and execute the user's selection.
    :param db:  The connection to the current database.
    :return:    None
    """
    list_action: str = ''
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
        exec(list_action)


def add_department(db):
    """
    Add a new student, making sure that we don't put in any duplicates,
    based on all the candidate keys (AKA unique indexes) on the
    students collection.  Theoretically, we could query MongoDB to find
    the uniqueness constraints in place, and use that information to
    dynamically decide what searches we need to do to make sure that
    we don't violate any of the uniqueness constraints.  Extra credit anyone?
    :param collection:  The pointer to the students collection.
    :return:            None
    """
    # Create a "pointer" to the students collection within the db database.
    collection = db["departments"]
    unique_name: bool = False
    unique_abbreviation: bool = False
    unique_chair_name: bool = False
    unique_building_office: bool = False
    unique_description: bool = False
    unique_department_chair: bool = False

    name: str = ''
    abbreviation: str = ''
    chair_name: str = ''
    building: str = ''
    office: int = 0
    description: str = ''

    while not unique_abbreviation or not unique_name:
        name = input("Department full name--> ")
        abbreviation = input("Department abbreviation--> ")
        name_count: int = collection.count_documents({"name": name})
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a department by that name.  Try again.")
        if unique_name:
            abbreviation_count = collection.count_documents({"abbreviation": abbreviation})
            unique_abbreviation = abbreviation_count == 0
            if not unique_abbreviation:
                print("We already have a department with that abbreviation.  Try again.")
    while not unique_chair_name:
        chair_name = input("Department chair name--> ")
        chair_name_count = collection.count_documents({"chair_name": chair_name})
        unique_chair_name = chair_name_count == 0
        if not unique_chair_name:
            print("We already have a department with that chair name. Try again.")

    while not unique_building_office:
        building = input("Department building--> ")
        office = int(input("Department Office--> "))
        building_office_count: int = collection.count_documents({"building": building, "office": office})
        unique_building_office = building_office_count == 0
        if not unique_building_office:
            print("We already have a department by that office in that building. Try again.")

    while not unique_description:
        description = input("Department description--> ")
        description_count: int = collection.count_documents({"description": description})
        unique_description = description_count == 0
        if not unique_description:
            print("We already have a department by that description. Try again.")

    # Build a new departments document preparatory to storing it
    department = {
        "name": name,
        "abbreviation": abbreviation,
        "chair_name": chair_name,
        "building": building,
        "office": office,
        "description": description,
        'courses': [],
        'majors': []
    }
    results = collection.insert_one(department)
    try:
        pass
    except Exception as e:
        print(e)
        add_department(db)


def select_department(db):
    """
    Select a student by the combination of the last and first.
    :param db:      The connection to the database.
    :return:        The selected student as a dict.  This is not the same as it was
                    in SQLAlchemy, it is just a copy of the Student document from
                    the database.
    """
    # Create a connection to the students collection from this database
    collection = db["departments"]
    found: bool = False
    name: str = ''
    abbreviation: str = ''
    while not found:
        name = input("Department's name--> ")
        abbreviation = input("Department's abbreviation--> ")
        name_count: int = collection.count_documents({"name": name, "abbreviation": abbreviation})
        found = name_count == 1
        if not found:
            print("No department found by that name and abbreviation.  Try again.")
    found_department = collection.find_one({"name": name, "abbreviation": abbreviation})
    return found_department


def delete_department(db):
    """
    Delete a student from the database.
    :param db:  The current database connection.
    :return:    None
    """
    # student isn't a Student object (we have no such thing in this application)
    # rather it's a dict with all the content of the selected student, including
    # the MongoDB-supplied _id column which is a built-in surrogate.
    department = select_department(db)
    # Create a "pointer" to the students collection within the db database.
    departments = db["departments"]
    # student["_id"] returns the _id value from the selected student document.
    deleted = departments.delete_one({"_id": department["_id"]})
    # The deleted variable is a document that tells us, among other things, how
    # many documents we deleted.
    print(f"We just deleted: {deleted.deleted_count} departments.")


def list_department(db):
    """
    List all of the students, sorted by last name first, then the first name.
    :param db:  The current connection to the MongoDB database.
    :return:    None
    """
    # No real point in creating a pointer to the collection, I'm only using it
    # once in here.  The {} inside the find simply tells the find that I have
    # no criteria.  Essentially this is analogous to a SQL find * from students.
    # Each tuple in the sort specification has the name of the field, followed
    # by the specification of ascending versus descending.
    departments = db["departments"].find({}).sort([("name", pymongo.ASCENDING),
                                                   ("abbreviation", pymongo.ASCENDING)])
    # pretty print is good enough for this work.  It doesn't have to win a beauty contest.
    for department in departments:
        pprint(department)


def add_course(db):
    """
    Add a new student, making sure that we don't put in any duplicates,
    based on all the candidate keys (AKA unique indexes) on the
    students collection.  Theoretically, we could query MongoDB to find
    the uniqueness constraints in place, and use that information to
    dynamically decide what searches we need to do to make sure that
    we don't violate any of the uniqueness constraints.  Extra credit anyone?
    :param collection:  The pointer to the students collection.
    :return:            None
    """

    # courses attr - departmentAbbreviation, department, courseNumber, name, description, units, sections
    # sections attr - course, departmentAbbreviation, courseNumber, sectionNumber, semester, sectionYear, building,
    #           room, schedule, startTime, instructor, students
    # student attr - studentID, lastName, firstName, email, majors, sections
    # majors attr - department, departmentAbbreviation, name, description, students
    # studentmajor attr - major, majorName, student, studentId, declarationDate
    # enrollment attr - enrollmentId, section, departmentAbbreviation, courseNumber, sectionNumber, sectionYear,
    #           semester, student, studentId, type
    # lettergrade - letterGradeId, grade
    # passfail - passFailId, applicationDate
    collection = db["courses"]
    is_dep: bool = False
    unique_number: bool = False
    unique_name: bool = False
    unique_desc: bool = False

    dep_abbr: str = ''
    name: str = ''
    number: int = 0
    description: str = ''
    units: int = 0
    while not unique_number or not unique_name or not unique_desc:
        dep_abbr = input("Department abbreviation--> ")
        number = int(input("Course number--> "))
        name = input("Course name--> ")
        description = input("Description--> ")
        units = int(input("Units--> "))
        dep_abbr_count: int = db["departments"].count_documents({"abbreviation": dep_abbr})
        is_dep = dep_abbr_count == 1
        if not is_dep:
            print("There is no department that goes by that abbreviation. Try again.")
        if is_dep:
            number_count: int = collection.count_documents({"course_number": number})
            unique_number = number_count == 0
            if not unique_number:
                print("We already have a course with that number. Try again.")
            if unique_number:
                name_count = collection.count_documents({"course_name": name})
                unique_name = name_count == 0
                if not unique_name:
                    print("We already have a course with that name. Try again.")
                if unique_name:
                    desc_count = collection.count_documents({"description": description})
                    unique_desc = desc_count == 0
                    if not unique_desc:
                        print("We already have that description for another department. Try again.")
    # Build a new courses document preparatory to storing it
    course = {
        "department_abbreviation": dep_abbr,
        "department": {"department_abbreviation": dep_abbr},
        "course_number": number,
        "course_name": name,
        "description": description,
        "units": units,
        "sections": []
    }
    try:
        results = collection.insert_one(course)
    except Exception as e:
        print(e)


def select_course(db):
    """
    Select a course by the name.
    :param db:      The connection to the database.
    :return:        The selected course as a dict.  This is not the same as it was
                    in SQLAlchemy, it is just a copy of the Student document from
                    the database.
    """
    # Create a connection to the departments collection from this database
    collection = db["courses"]
    found: bool = False
    unique_abbr: bool = False
    number: int = 0
    while not found or not unique_abbr:
        dep_abbr = input("Department abbreviation--> ")
        number = int(input("Course's number--> "))
        abbr_count: int = collection.count_documents({"department_abbreviation": dep_abbr})
        unique_abbr = abbr_count == 1
        if not unique_abbr:
            print("No department found by that abbreviation. Try again.")
        if unique_abbr:
            number_count: int = collection.count_documents({"course_number": number})
            found = number_count == 1
            if not found:
                print("No courses found by that number.  Try again.")
    found_course = collection.find_one({"course_number": number})
    return found_course


def delete_course(db):
    """
    Delete a department from the database.
    :param db:  The current database connection.
    :return:    None
    """
    # student isn't a Student object (we have no such thing in this application)
    # rather it's a dict with all the content of the selected student, including
    # the MongoDB-supplied _id column which is a built-in surrogate.
    course = select_course(db)
    has_children: bool = False
    # Create a "pointer" to the students collection within the db database.
    courses = db["courses"]
    departments = db["departments"]
    for i in db['sections'].find({}):
        if i['course_number'] == course['course_number']:
            has_children = True
    # student["_id"] returns the _id value from the selected student document.
    if has_children != True:
        deleted = courses.delete_one({"_id": course["_id"]})
        departments.update_one({"abbreviation": course["department_abbreviation"]},
                               {'$pull': {'courses': course['course_number']}})
        print(f"We just deleted: {deleted.deleted_count} course(s).")

    if has_children == True:
        print("There are still sections in this course. Please delete them first before deleting the course.")


def list_course(db):
    """
    List all of the students, sorted by last name first, then the first name.
    :param db:  The current connection to the MongoDB database.
    :return:    None
    """
    courses = db["courses"].find({}).sort([("department_abbreviation", pymongo.ASCENDING)])
    for course in courses:
        pprint(course)


def list_department_courses(db):
    department = select_department(db)
    for i in department["courses"]:
        found_course = db["courses"].find_one({"course_number": i})
        pprint(found_course)


def add_enrollment(db):
    collection = db["sections"]
    student = select_student(db)
    section = select_section(db)
    enrollment = section['enrollment']
    pass_fail: datetime
    decision = input("Is this student to be graded by pass/fail? Input 'y' or 'n' --> ")
    if decision == "y":
        pass_fail = datetime.now().date()
        collection.update_one({"_id": section['_id']}, {"$push": {"enrollment": {"student": student, "pass_fail": pass_fail}}})
    elif decision == "n":
        letter_grade = input("What is considered a satisfactory grade for this student? Input A, B or C ---> ")
        collection.update_one({"_id": section['_id']}, {"$push": {"enrollment": {"student": student, "letter_grade": letter_grade}}})

def list_enrollments(db):
    section = select_section(db)
    for student in section.enrollments.student:
        print(student)

def delete_enrollment(db):
    collection = db["sections"]
    section = select_section(db)
    student = select_student(db)
    sections.update_one(
        {'_id': section['_id']}, {"$pull": {"enrollment": {"student": student}}}
    )

def add_section(db):
    collection = db["sections"]
    is_dep: bool = False
    is_course: bool = False
    unique_number: bool = False
    unique_constraint1: bool = False
    unique_constraint2: bool = False

    section_number: int = 0
    semester: str = ''
    section_year: int = 0
    schedule: str = ''
    start_time: time
    instructor: str = ''
    building: str = ''
    room: int = 0
    while not is_dep or not is_course or not unique_number or not unique_constraint1 or not unique_constraint2:
        dep_abbr = input("Department abbreviation--> ")
        dep_abbr_count: int = db["departments"].count_documents({"abbreviation": dep_abbr})
        is_dep = dep_abbr_count == 1
        if not is_dep:
            print("There is no department that goes by that abbreviation. Try again.")
        if is_dep:
            course_num = int(input("Course number--> "))
            course_count: int = db["courses"].count_documents({"course_number": course_num})
            is_course = course_count == 1
            if not is_course:
                print("There is no course with that number. Try again.")
            if is_course:
                section_number = int(input("Section Number--> "))
                semester = input("Semester--> ")
                section_year = int(input("Section Year--> "))
                schedule = input("Schedule--> ")
                # start_time_str = input("Start Time (HH:MM)--> ")
                start_time_str = input("Enter a start time as HHMM for a 24-hour clock--> ")
                try:
                    start_time = datetime.strptime(start_time_str, "%H%M")
                except ValueError:
                    print("Invalid time format. Please use HH:MM format. Try again.")
                    continue
                instructor = input("Instructor--> ")
                building = input("Building--> ")
                room = int(input("Room Number--> "))
                section_number_count: int = collection.count_documents({'department_abbreviation': dep_abbr,
                                                                        'course_number': course_num,
                                                                        'section_number': section_number})
                unique_number = section_number_count == 0
                if not unique_number:
                    print("We already have a section with that section number in this course. Try again.")
                if unique_number:
                    constraint1_count: int = collection.count_documents({'department_abbreviation': dep_abbr,
                                                                         'course_number': course_num,
                                                                         'section_year': section_year,
                                                                         'semester': semester,
                                                                         'start_time': start_time,
                                                                         'instructor': instructor})
                    unique_constraint1 = constraint1_count == 0
                    if not unique_constraint1:
                        print("We already have a section with those inputs. Try again.")
                    if unique_constraint1:
                        constraint2_count: int = collection.count_documents({'department_abbreviation': dep_abbr,
                                                                             'course_number': course_num,
                                                                             'section_year': section_year,
                                                                             'semester': semester,
                                                                             'start_time': start_time,
                                                                             'building': building,
                                                                             'room': room})
                        unique_constraint2 = constraint2_count == 0
                        if not unique_constraint2:
                            print("We already have a section with that building and room with those inputs. Try again.")

    # Build a new courses document preparatory to storing it
    section = {
        "department_abbreviation": dep_abbr,
        "course_number": course_num,
        "section_number": section_number,
        "semester": semester,
        "section_year": section_year,
        "building": building,
        "room": room,
        "schedule": schedule,
        "start_time": start_time,
        "instructor": instructor,
        "enrollments": [],
        "course": [],
        "department": {"department_abbreviation": dep_abbr}
    }
    try:
        results = collection.insert_one(section)
        db["courses"].update_one({'course_number': course_num}, {'$push': {'sections': section_number}})
        print('Successfully added a section!')
    except Exception as e:
        print(e)


def select_section(db):
    """
    Select a course by the name.
    :param db:      The connection to the database.
    :return:        The selected course as a dict.  This is not the same as it was
                    in SQLAlchemy, it is just a copy of the Student document from
                    the database.
    """
    # Create a connection to the departments collection from this database
    collection = db["sections"]
    found: bool = False
    unique_course: bool = False
    unique_abbr: bool = False
    dep_abbr: str = ''
    course_num: int = 0
    section_num: int = 0
    semester: str = ''
    sectionYear: int = 0
    while not found or not unique_course or unique_abbr:
        dep_abbr = input("Department abbreviation--> ")
        abbr_count: int = collection.count_documents({"department_abbreviation": dep_abbr})
        unique_abbr = abbr_count == 1
        if not unique_abbr:
            print("No department found by that abbreviation. Try again.")
        if unique_abbr:
            course_num = int(input("Course's number--> "))
            course_count: int = collection.count_documents({"course_number": course_num})
            unique_course = course_count == 1
            if not unique_course:
                print("No course found by that number. Try again.")
            if unique_course:
                section_num = int(input("Section's number--> "))
                semester = input("Semester--> ")
                sectionYear = int(input('Which year is this section offered in? --> '))
                pk_count: int = collection.count_documents({'department_abbreviation': dep_abbr,
                                                            'course_number': course_num,
                                                            'section_number': section_num,
                                                            'semester': semester,
                                                            'section_year': sectionYear})
                found = pk_count == 1
                if not found:
                    print("No section found by that department, course, section#, semester, and year. Try again.")
    found_section = collection.find_one({"department_abbreviation": dep_abbr, "course_number": course_num,
                                         "section_number": section_num, "semester": semester,
                                         "section_year": sectionYear})
    return found_section


def delete_section(db):
    section = select_section(db)
    print('found section')
    # Create a "pointer to the students collection within the db database.
    sections = db["sections"]
    courses = db["courses"]
    # student["_id"] returns the _id value from the selected student document.
    deleted = sections.delete_one({"_id": section["_id"]})
    courses.update_one({"course_number": sections["course_number"]},
                       {'$pull': {'sections': section['section_number']}})
    # The deleted variable is a document that tells us, among other things, how
    # many documents we deleted.
    print(f"We just deleted: {deleted.deleted_count} section(s).")


def list_course_sections(db):
    """
    List all of the students, sorted by last name first, then the first name.
    :param db:  The current connection to the MongoDB database.
    :return:    None
    """
    course = select_course(db)
    # No real point in creating a pointer to the collection, I'm only using it
    # once in here.  The {} inside the find simply tells the find that I have
    # no criteria.  Essentially this is analogous to a SQL find * from students.
    # Each tuple in the sort specification has the name of the field, followed
    # by the specification of ascending versus descending.
    for i in course["sections"]:
        found_section = db["sections"].find_one({"section_number": i})
        pprint(found_section)


def add_student(db):
    collection = db["students"]
    majors_collection = db["majors"]
    departments_collection = db["departments"]

    unique_id: bool = False
    unique_name: bool = False
    unique_email: bool = False

    last_name: str = ''
    first_name: str = ''
    email: str = ''
    _id: int = 0

    while not unique_id or not unique_name or not unique_email:
        last_name = input("Student last name--> ")
        first_name = input("Student first name--> ")
        email = input("Student e-mail address--> ")
        _id = int(input("Student ID--> "))

        # Check if student ID is unique
        id_count: int = collection.count_documents({"_id": _id})
        unique_id = id_count == 0
        if not unique_id:
            print("We already have a student with that ID. Try again.")
            continue

        # Check if student name is unique
        name_count: int = db["students"].count_documents({"last_name": last_name, "first_name": first_name})
        unique_name = name_count == 0
        if not unique_name:
            print("There is already a student with that name. Try again.")
            continue

        # Check if student email is unique
        email_count: int = collection.count_documents({"email": email})
        unique_email = email_count == 0
        if not unique_email:
            print("We already have a student who has that email address. Try again.")
            continue

    student = {
        "_id": _id,
        "last_name": last_name,
        "first_name": first_name,
        "email": email,
        "student_majors": []
    }

    # Add major declaration
    while True:
        major_name = input("Major name--> ")
        declaration_date_str = input("Declaration date (YYYY-MM-DD)--> ")

        try:
            # Parse declaration date string to datetime object
            declaration_date = datetime.strptime(declaration_date_str, "%Y-%m-%d")

            # Check if the major exists in the majors collection
            major_exists = majors_collection.count_documents({"major_name": major_name}) > 0
            if not major_exists:
                print("Error: This major does not exist. Please add the major to the department first.")
                continue

            # Add major declaration to student document
            student["student_majors"].append({"declaration_date": declaration_date, "major": {"name": major_name}})
            break
        except ValueError:
            print("Invalid date format. Please enter date in YYYY-MM-DD format.")
            continue

    try:
        # Insert student into the students collection
        results = collection.insert_one(student)
        print('Successfully added a student!')
    except Exception as e:
        print(e)


def select_student(db):
    collection = db["students"]
    found: bool = False
    last_name: str = ''
    first_name: str = ''
    while not found:
        last_name = input("Student's last name--> ")
        first_name = input("Student's first name--> ")
        name_count: int = collection.count_documents({"last_name": last_name, "first_name": first_name})
        found = name_count == 1
        if not found:
            print("No students found by that name.  Try again.")
    found_student = collection.find_one({"last_name": last_name, "first_name": first_name})
    return found_student


def delete_student(db):
    student = select_student(db)
    students = db["students"]
    majors = db["majors"]
    deleted = students.delete_one({"_id": student["_id"]})
    print(f"We just deleted: {deleted.deleted_count} student(s).")


def list_student(db):
    students = db["students"].find({}).sort([("_id", pymongo.ASCENDING)])
    for student in students:
        pprint(student)


def add_major(db):
    collection = db["majors"]
    unique_name: bool = False
    unique_desc: bool = False

    department_abbr: str = ''
    name: str = ''
    description: str = ''

    while not unique_name or not unique_desc:
        department_abbr = input("Department abbreviation--> ")
        name = input("Major name--> ")
        description = input("Description--> ")

        # Check if the department abbreviation exists
        dep_abbr_count: int = db["departments"].count_documents({"abbreviation": department_abbr})
        if dep_abbr_count == 0:
            print("There is no department that goes by that abbreviation. Try again.")
            continue

        # Check uniqueness of major name
        name_count = collection.count_documents({"major_name": name})
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a major with that name. Try again.")
            continue

        # Check uniqueness of description
        desc_count = collection.count_documents({"description": description})
        unique_desc = desc_count == 0
        if not unique_desc:
            print("We already have that description for another major. Try again.")
            continue

    major = {
        "department_abbreviation": department_abbr,
        "major_name": name,
        "description": description
    }

    try:
        # Insert major into the majors collection
        results = collection.insert_one(major)
        # Update the corresponding department document to include the new major
        db["departments"].update_one({'abbreviation': department_abbr}, {'$push': {'majors': name}})
        print('Successfully added a major!')
    except Exception as e:
        print(e)


def select_major(db):
    collection = db["majors"]
    found: bool = False
    name: str = ''
    while not found:
        name = input("Major's name--> ")
        name_count: int = collection.count_documents({"major_name": name})
        found = name_count == 1
        if not found:
            print("No majors found by that name.  Try again.")
    found_major = collection.find_one({"major_name": name})
    return found_major


def delete_major(db):
    major = select_major(db)
    # Create a "pointer" to the students collection within the db database.
    majors = db["majors"]
    departments = db["departments"]
    # student["_id"] returns the _id value from the selected student document.
    deleted = majors.delete_one({"_id": major["_id"]})
    departments.update_one({"abbreviation": major["department_abbreviation"]},
                           {'$pull': {'majors': major['major_name']}})
    # The deleted variable is a document that tells us, among other things, how
    # many documents we deleted.
    print(f"We just deleted: {deleted.deleted_count} major(s).")


def list_major(db):
    majors = db["majors"].find({}).sort([("department_abbreviation", pymongo.ASCENDING)])
    for major in majors:
        pprint(major)


if __name__ == '__main__':
    cluster = "mongodb+srv://tristenseng:backpack@cluster0.bis7cwk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(cluster)
    # As a test that the connection worked, print out the database names.
    print(client.list_database_names())
    # db will be the way that we refer to the database from here on out.

    # Print off the collections that we have available to us, again more of a test than anything.
    print(db.list_collection_names())
    # student is our students collection within this database.
    # Merely referencing this collection will create it, although it won't show up in Atlas until
    # we insert our first document into this collection.
    departments = db["departments"]
    department_count = departments.count_documents({})

    # ************************** Set up the students collection
    departments_indexes = departments.index_information()
    if 'departments_abbreviations' in departments_indexes.keys():
        print("abbreviation index present.")
    else:
        # Create a single UNIQUE index on BOTH the last name and the first name.
        departments.create_index([('abbreviation', pymongo.ASCENDING)], unique=True, name="departments_abbreviations")

    if 'departments_chair_names' in departments_indexes.keys():
        print("chair name index present.")
    else:
        # Create a UNIQUE index on just the e-mail address
        departments.create_index([('chair_name', pymongo.ASCENDING)], unique=True, name='departments_chair_names')

    if 'departments_buildings_and_offices' in departments_indexes.keys():
        print("building and office index present.")
    else:
        # Create a single UNIQUE index on BOTH the last name and the first name.
        departments.create_index([('building', pymongo.ASCENDING), ('office', pymongo.ASCENDING)],
                                 unique=True, name="departments_buildings_and_offices")

    if 'departments_descriptions' in departments_indexes.keys():
        print("description index present.")
    else:
        departments.create_index([('description', pymongo.ASCENDING)], unique=True, name="departments_descriptions")

    pprint(departments.index_information())
    # ************************** Set up the courses collection
    courses = db["courses"]
    course_count = courses.count_documents({})
    courses_indexes = courses.index_information()
    if 'courses_uk_01' in courses_indexes.keys():
        print("department abbreviation/course number index present.")
    else:
        courses.create_index([('department_abbreviation', pymongo.ASCENDING), ('course_number', pymongo.ASCENDING)],
                             unique=True, name='courses_uk_01')
    if 'courses_uk_02' in courses_indexes.keys():
        print("department abbreviation/course name index present.")
    else:
        courses.create_index([('department_abbreviation', pymongo.ASCENDING), ('course_name', pymongo.ASCENDING)],
                             unique=True, name='courses_uk_02')
    pprint(courses.index_information())
    # ************************** Set up the sections collection
    sections = db["sections"]
    section_count = sections.count_documents({})
    sections_indexes = sections.index_information()
    if 'sections_uk_01' in sections_indexes.keys():
        print("course-section number-semester-year index present.")
    else:
        sections.create_index([('course', pymongo.ASCENDING), ('section_number', pymongo.ASCENDING),
                               ('semester', pymongo.ASCENDING), ('section_year', pymongo.ASCENDING)],
                              unique=True, name='sections_uk_01')
    if 'sections_uk_02' in sections_indexes.keys():
        print("semester-year-building-room-schedule-start time index present.")
    else:
        sections.create_index([('semester', pymongo.ASCENDING), ('section_year', pymongo.ASCENDING),
                               ('building', pymongo.ASCENDING), ('room', pymongo.ASCENDING),
                               ('schedule', pymongo.ASCENDING), ('start_time', pymongo.ASCENDING)],
                              unique=True, name='sections_uk_02')
    if 'sections_uk_03' in sections_indexes.keys():
        print("semester-year-schedule-start time-instructor index present.")
    else:
        sections.create_index([('semester', pymongo.ASCENDING), ('section_year', pymongo.ASCENDING),
                               ('schedule', pymongo.ASCENDING), ('start_time', pymongo.ASCENDING),
                               ('instructor', pymongo.ASCENDING)],
                              unique=True, name='sections_uk_03')
    # if 'sections_uk_05' in sections_indexes.keys():
    #    print("semester-year-dept abbreviation-course number-student id index present.")

    # else:
    #    sections.create_index([('semester', pymongo.ASCENDING), ('section_year', pymongo.ASCENDING),
    #                           ('department.department_abbreviation', pymongo.ASCENDING),
    #                           ('course.course_number', pymongo.ASCENDING),
    #                           ('enrollments.students.student_id', pymongo.ASCENDING)],
    #                          unique=True, name='sections_uk_05')
    pprint(sections.index_information())
    main_action: str = ''
    while main_action != menu_main.last_action():
        main_action = menu_main.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)

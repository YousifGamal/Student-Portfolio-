class User:
    def __init__(self, username, password =None , type = None, email = None):
        self.username: str = username
        self.password: str = password
        self.type: str = type
        self.email: str = email

class Course:
    def __init__(self, name, code, year):
        self.name: str = name
        self.code: str = code
        self.year: int = year

class Student:
    def __init__(self, name, section_no, bn, current_year, username):
        self.name: str = name
        self.section_no: int = section_no
        self.bn: int = bn
        self.current_year: int = current_year
        self.username: str = username

class StaffMember:
    def __init__(self, name, department, username):
        self.name: str = name
        self.username: str = username
        self.department: str = department

class Semester:
    def __init__(self, semester, year):
        self.semester = semester
        self.year = year

class Requirement:
    def __init__(self, id, course_code, project_id, name, deadline, additional_materials, document, type, members_number):
        self.id = id
        self.course_code = course_code
        self.project_id = project_id
        self.name = name
        self.deadline = deadline
        self.additional_materials = additional_materials
        self.document = document
        self.type = type
        self.members_number = members_number

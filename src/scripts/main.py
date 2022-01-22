from dataclasses import dataclass, field, asdict
import json
import course_scrape as cs



@dataclass(slots=True)
class Assignment:
    id: int = 0
    course: str = ""
    name: str = ""
    dueDate: str = ""
    dueTime: str = ""
    submissionPlatform: str = ""
    submissionPlatformURL: str = ""


@dataclass(slots=True)
class Exam:
    id: int = 0
    weight: int = 0
    type: str = ""
    date: str = ""
    time: str = ""
    location: str = ""
    durationHour: int = 0
    durationMin: int = 0


@dataclass(slots=True)
class Course:
    courseID: int = 0
    subject: str = ""
    faculty: str = ""
    courseNb: int = 0
    title: str = ""
    crn: int = 0
    semester: str = ""
    type: str = ""
    credit: int = 0
    year: int = 0
    section: int = 0
    location: str = ""
    days: str = ""
    instructor: str = ""
    startTime: str = ""
    endTime: str = ""
    assignments: list = field(default_factory=list)
    exams: list = field(default_factory=list)

    def add_assignment(self, assignment):
        self.assignments.append(assignment)

    def add_exam(self, exam):
        self.exams.append(exam)

    def to_json(self):
        return json.dumps(asdict(self))


@dataclass(slots=True)
class User:
    id: int = 0
    first_name: str = ""
    last_name: str = ""
    email: str = ""

    def to_json(self):
        return json.dumps(asdict(self))


assignment1 = Assignment()
assignment1.course = "COMP 321"
assignment1.name = "Assignment 1"
assignment1.dueDate = "January 22 2022"
assignment1.dueTime = "9pm"
assignment1.submissionPlatform = "Crowdmark"
assignment2 = Assignment()
user1 = User()
user1.id = 1
user1.first_name = "John"
user1.last_name = "Doe"
user1.email = "johndoe@gmail.com"
course1 = Course()
course1.add_assignment(assignment1)
course1.add_assignment(assignment2)

#print(course1.to_json())

cs.get_schedule("nicholas.corneau@mail.mcgill.ca", "nick51199")



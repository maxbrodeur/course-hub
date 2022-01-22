from dataclasses import dataclass, field, asdict
import json
import course_scrape as cs


@dataclass(slots=True)
class Assignment:
    course: str = ""
    name: str = ""
    dueDate: str = ""
    dueTime: str = ""
    submissionPlatform: str = ""
    submissionPlatformURL: str = ""


@dataclass(slots=True)
class Exam:
    weight: int = 0
    type: str = ""
    date: str = ""
    time: str = ""
    location: str = ""
    durationHour: int = 0
    durationMin: int = 0


@dataclass(slots=True)
class Course:
    subject: str = ""
    faculty: str = ""
    courseNb: int = 0
    title: str = ""
    crn: int = 0
    semester: str = ""
    type: str = ""
    credit: int = 0
    year: int = 0
    section: str = ""
    location: str = ""
    monday: bool = False
    tuesday: bool = False
    wednesday: bool = False
    thursday: bool = False
    friday: bool = False
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
    first_name: str = ""
    last_name: str = ""
    email: str = ""

    def to_json(self):
        return json.dumps(asdict(self))


# course_list = cs.get_schedule("nicholas.corneau@mail.mcgill.ca", "nick51199")

def find_days(course, days):
    if days[0] == "M":
        course.monday = True
    elif days[0] == "T":
        course.tuesday = True
    elif days[0] == "W":
        course.wednesday = True
    elif days[0] == "R":
        course.thursday = True
    else:
        course.friday = True

    if len(days) >= 2:
        if days[1] == "M":
            course.monday = True
        elif days[1] == "T":
            course.tuesday = True
        elif days[1] == "W":
            course.wednesday = True
        elif days[1] == "R":
            course.thursday = True
        else:
            course.friday = True

    if len(days) >= 3:
        if days[2] == "M":
            course.monday = True
        elif days[2] == "T":
            course.tuesday = True
        elif days[2] == "W":
            course.wednesday = True
        elif days[2] == "R":
            course.thursday = True
        else:
            course.friday = True

    if len(days) >= 4:
        if days[3] == "M":
            course.monday = True
        elif days[3] == "T":
            course.tuesday = True
        elif days[3] == "W":
            course.wednesday = True
        elif days[3] == "R":
            course.thursday = True
        else:
            course.friday = True

    if len(days) >= 5:
        if days[4] == "M":
            course.monday = True
        elif days[4] == "T":
            course.tuesday = True
        elif days[4] == "W":
            course.wednesday = True
        elif days[4] == "R":
            course.thursday = True
        else:
            course.friday = True


def get_courses_information():
    new_course_list = []

    for course in course_list:
        new_course = Course()
        find_days(new_course, course["day"])
        new_course.subject = course["subject"][1:5]
        new_course.courseNb = course["subject"][6:9]
        new_course.title = course["title"][:-1]
        new_course.crn = course["crn"]
        new_course.semester = course["term"][:-5]
        new_course.type = course["type"]
        new_course.credit = course["credit"][0:1]
        new_course.year = course["term"][len(course["term"])-4:]
        new_course.section = course["section"][1:]
        new_course.location = course["location"]

        if "instructor" in course:
            new_course.instructor = course["instructor"]

        else:
            new_course.instructor = course["instructors"]

        new_course.startTime = course["times"]



course1 = Course()
find_days(course1, "F")
print(course1.monday)
print(course1.tuesday)
print(course1.wednesday)
print(course1.thursday)
print(course1.friday)
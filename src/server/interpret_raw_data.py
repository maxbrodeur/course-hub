from dataclasses import dataclass, field, asdict
import json
import course_scrape as cs
from datetime import datetime, time
from dbController import *

secrets = open("../../assets/secrets.txt").readlines()
email = secrets[0][:-1]
password = secrets[1]


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
    startTime: time = time
    endTime: time = time
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
    courses: list = field(default_factory=list)

    def to_json(self):
        return json.dumps(asdict(self))


def find_days(course, days):
    if "M" in days:
        course.monday = True
    if "T" in days:
        course.tuesday = True
    if "W" in days:
        course.wednesday = True
    if "R" in days:
        course.thursday = True
    if "F" in days:
        course.friday = True


def find_times(course, times):
    new_times = times.split(" - ")
    start_time_hour = new_times[0].split(" ")[0].split(":")[0]
    start_time_min = new_times[0].split(" ")[0].split(":")[1]
    start_time_noon = new_times[0].split(" ")[1]
    end_time_hour = new_times[1].split(" ")[0].split(":")[0]
    end_time_min = new_times[1].split(" ")[0].split(":")[1]
    end_time_noon = new_times[1].split(" ")[1]

    if start_time_noon == "am" or (start_time_noon == "pm" and start_time_hour == "12"):
        start_time = f"{start_time_hour}:{start_time_min}"
        course.startTime = datetime.datetime.strptime(start_time, "%H:%M").time()

    else:
        start_time = f"{str(int(start_time_hour) + 12)}:{start_time_min}"
        course.startTime = datetime.datetime.strptime(start_time, "%H:%M").time()

    if end_time_noon == "am" or (end_time_noon == "pm" and end_time_hour == "12"):
        end_time = f"{end_time_hour}:{end_time_min}"
        course.endTime = datetime.datetime.strptime(end_time, "%H:%M").time()

    else:
        end_time = f"{str(int(end_time_hour) + 12)}:{end_time_min}"
        course.endTime = datetime.datetime.strptime(end_time, "%H:%M").time()


def get_courses_information(course_list):
    new_course_list = []

    for course in course_list:
        new_course = Course()
        find_days(new_course, course["day"])
        find_times(new_course, course["times"])
        new_course.subject = course["subject"][1:5]
        new_course.courseNb = int(course["subject"][6:9])
        new_course.title = course["title"][:-1]
        new_course.crn = int(course["crn"])
        new_course.semester = course["term"][:-5]
        new_course.type = course["type"]
        new_course.credit = int(course["credits"][0:1])
        new_course.year = int(course["term"][len(course["term"]) - 4:])
        new_course.section = course["section"][1:]
        new_course.location = course["location"]

        if "instructor" in course:
            new_course.instructor = course["instructor"]

        else:
            new_course.instructor = course["instructors"]

        new_course_list.append(asdict(new_course))

    return new_course_list


if __name__ == "__main__":
    course_list = cs.get_schedule(email, password)
    new_course_list = get_courses_information(course_list)
    db = dbController()
    count = 0
    for course in new_course_list:
        try:
            db.add_course(course)
        except psycopg2.errors.UniqueViolation:
            count += 1

    if count != 0:
        print(f"{count} courses already exist")


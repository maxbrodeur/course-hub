from dataclasses import dataclass, field


@dataclass(slots=True)
class Assignments:
    ID: int = 0
    assignmentNumber: int = 0
    dueDate: str = ""
    dueTime: str = ""
    submissionPlatform: str = ""
    submissionPlatformURL: str = ""


@dataclass(slots=True)
class Course:
    courseID: int = 0
    subject: str = ""
    faculty: str = ""
    courseNumber: int = 0
    title: str = ""
    crn: int = 0
    semester: str = ""
    credit: int = 0
    year: int = 0
    section: int = 0
    location: str = ""
    days: list = field(default_factory=list)
    instructor: str = ""
    startTime: str = ""
    endTime: str = ""
    assignments: list = field(default_factory=list)




@dataclass(slots=True)
class User:
    ID: int = 0
    firstName: str = ""
    lastName: str = ""




import datetime
import pytest
from server.dbController import *
import uuid

def test_addDeletecourse():
    controller = dbController()
    x= {
        "subject": "comp",
        "faculty": "eng",
        "courseNb": "250",
        "title":"Intro to computer science",
        "crn":000,
        "semester": "winter",
        "type": "lecture",
        "credit": 3,
        "year": 2022,
        "section": 1,
        "location":"building x",
        "monday": True,
        "tuesday": False,
        "wednesday": True,
        "thursday": False,
        "friday": True,
        "instructor": "Mr.Bean",
        "startTime": datetime.time(10, 30),
        "endTime": datetime.time(11,30)
    }
    controller.add_course(x)
    assert controller.getRowCount() == 1
    controller.setRowCount(0)
    controller.delete_course(000)
    assert controller.getRowCount() == 1

def test_addDeleteUser():
    controller = dbController()
    x = {
        "firstname": "John",
        "lastname": "doe",
        "email": "jon@doe",
        "studentid": 433421
    }
    controller.add_user(x)
    assert controller.getRowCount() == 1
    controller.setRowCount(0)
    controller.delete_user("jon@doe")
    assert controller.getRowCount() == 1

def test_addDeleteAssignment():
    controller = dbController()
    id = controller.adaptUUID(uuid.uuid4())
    x = {
        "course": id,
        "name": "ass1",
        "dueDate": datetime.date(2022,1,1),
        "dueTime": datetime.time(12,00),
        "submissionPlatform": "ed",
        "submissionPlatformURL": "lkin"
    }
    id = controller.add_assignment(x)
    assert controller.getRowCount() == 1
    controller.setRowCount(0)
    controller.delete_assignment(id)
    assert controller.getRowCount() == 1

def test_addDeleteExam():
    controller = dbController()
    id = controller.adaptUUID(uuid.uuid4())
    x = {
        "course": id,
        "weight": 30,
        "type": "quiz",
        "date": datetime.date(2022, 1, 1),
        "time": datetime.time(12,0),
        "location": "building",
        "duration": datetime.timedelta(hours=3)
    }
    id = controller.add_exam(x)
    assert controller.getRowCount() == 1
    controller.setRowCount(0)
    controller.delete_exam(id)
    assert controller.getRowCount() == 1

def test_getCourse():
    controller = dbController()
    x= {
        "subject": "comp",
        "faculty": "eng",
        "courseNb": "250",
        "title":"Intro to computer science",
        "crn":250,
        "semester": "winter",
        "type": "lecture",
        "credit": 3,
        "year": 2022,
        "section": 1,
        "location":"building x",
        "monday": True,
        "tuesday": False,
        "wednesday": True,
        "thursday": False,
        "friday": True,
        "instructor": "Mr.Bean",
        "startTime": datetime.time(10, 30),
        "endTime": datetime.time(11,30)
    }
    controller.add_course(x)
    assert (controller.getCourse(250))[5] == 250
    controller.delete_course(250)
    assert controller.getRowCount() == 1
    

    


#!/usr/bin/env python3

import psycopg2;
from psycopg2.errors import SerializationFailure
import json
import logging

class dbController:

    def __init__(self):
        self.connect()
    
    def connect(self):
        self.conn = psycopg2.connect(
            database = 'course-hub-db-5540.coursehub',
            user = 'magix022',
            host = 'free-tier.gcp-us-central1.cockroachlabs.cloud',
            port = 26257,
            password = 'dyYDcwElWi4tbbhjnkRobA'
        )
    def add_course(self,jsonObject):
        if(self.conn.closed != 0):
            self.connect()
        disc = json.loads(jsonObject)
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO courses VALUES ( '{0}', '{1}', {2}, '{3}', {4}, '{5}', '{6}', {7}, {8}, {9}, '{10}', {11}, {12}, {13}, {14}, {15}, '{16}', {17}, {18} )".format(
                    disc["subject"], #0
                    disc["faculty"], #1
                    disc["courseNb"], #2
                    disc["title"], #3
                    disc["crn"], #4
                    disc["semester"], #5
                    disc["type"], #6
                    disc["credit"], #7
                    disc["year"], #8
                    disc["section"], #9
                    disc["location"], #10
                    disc["monday"], #11
                    disc["tuesday"], #12
                    disc["wednesday"], #13
                    disc["thursday"], #14
                    disc["friday"], #15
                    disc["instructor"], #16
                    disc["startTIme"], #17
                    disc["endTime"] #18
                )
            )
            logging.debug("add_course(): status message: %s", cur.statusmessage)
        self.conn.commit()

    def add_user(self, jsonObject):
        if(self.conn.closed != 0):
            self.connect()
        disc = json.loads(jsonObject)
        with self.conn.cursor() as cur:
            str = "INSERT INTO users (firstname, lastname, email, studentid) VALUES ( '{0}', '{1}', '{2}', {3})".format(
                    disc["firstname"],
                    disc["lastname"],
                    disc["email"],
                    disc["studentid"]
                )
            cur.execute(
                str
            ) 
            logging.debug("add_user(): status nmessage: %s", cur.statusmessage)
        self.conn.commit()
    
    def add_assignment(self, jsonObject):
        if(self.conn.closed):
            self.connect()
        disc = json.loads(jsonObject)
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO assignment VALUES ( {0}, '{1}', {2}, {3}, '{4}', '{5}')".format(
                    disc["course"],
                    disc["name"],
                    disc["dueDate"],
                    disc["dueTime"],
                    disc["submissionPlatform"],
                    disc["submissionPlatformURL"]
                )
            )
            logging.debug("add_assignment(): status message: %s", cur.statusmessage)
        self.conn.commit()

    def add_exam(self, jsonObject):
        if(self.conn.closed):
            self.connect()
        disc = json.loads(jsonObject)
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO exams VALUES ( {0}, {1}, '{2}', {3}, {4}, '{5}', {6})".format(
                    disc["course"],
                    disc["weight"],
                    disc["type"],
                    disc["date"],
                    disc["time"],
                    disc["location"],
                    disc["duration"]
                )
            )
            logging.debug("add_exam(): status message: %s", cur.statusmessage)
        self.conn.commit()

    def main(self):
        x = {
            "firstname": "john",
            "lastname": "doe",
            "email": "johndoegmail.com",
            "studentid": 239231291
        }
        y = json.dumps(x)
        self.connect()
        print("Connected")
        self.add_user(y)
        print(self.conn.closed)
        self.conn.close()


if __name__ == "__main__":
    controller = dbController()
    controller.main()

    

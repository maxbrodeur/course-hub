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
                "INSERT INTO courses VALUES ( {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17}, {18}, {19}, {20} )".format(
                    disc["courseID"],
                    disc["subject"],
                    disc["faculty"],
                    disc["courseNb"],
                    disc["title"],
                    disc["crn"],
                    disc["semester"],
                    disc["type"],
                    disc["credit"],
                    disc["year"],
                    disc["section"],
                    disc["location"],
                    disc["monday"],
                    disc["tuesday"],
                    disc["wednesday"],
                    disc["thursday"],
                    disc["friday"],
                    disc["instructor"],
                    disc["startTIme"],
                    disc["endTime"]
                )
            )
            logging.debug("add_course(): status message: %s", cur.statusmessage)
        self.conn.commit()

    def add_user(self, jsonObject):
        if(self.conn.closed != 0):
            self.connect()
        disc = json.loads(jsonObject)
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users VALUES ( {1}, {2}, {3}, {4}".format(
                    disc["id"],
                    disc["first_name"],
                    disc["last_name"],
                    disc["email"]
                )
            ) 
            logging.debug("add_user(): status nmessage: %s", cur.statusmessage)
        self.conn.commit()
    
    def add_assignment(self, jsonObject):
        if(self.conn.closed):
            self.connect()
        disc = json.loads(jsonObject)
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO assignment VALUES ( {1}, {2}, {3}, {4}, {5}, {6}, {7}".format(
                    disc["id"],
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
                "INSERT INTO exams VALUES ( {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}".format(
                    disc["id"],
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
        self.connect()
        print("Connected")
        self.conn.close()


if __name__ == "__main__":
    controller = dbController()
    controller.main()

    

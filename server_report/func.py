#!python3
import globus_sdk
import pickle
import os
from subprocess import call
import sys
import sqlite3 as lite
import server_report.auth as auth
import logging

log = logging.getLogger(__name__)

def list_endpoints():
    log.info("Aquiring access token from refresh token...")
    tc = auth.authenticate()
    print("My Managed Endpoints:")
    for ep in tc.endpoint_manager_monitored_endpoints():
        print("[{}] {}".format(ep["id"], ep["display_name"]))

def user_frequency(endpointid, startdate, enddate):
    log.info("Aquiring access token from refresh token...")
    tc = auth.authenticate()
    log.info("Creating database in memory...")
    con = lite.connect(':memory:')
    with con:
        cur = con.cursor()
        log.info("Creating Table...")
        cur.execute("CREATE TABLE People(Name TEXT, Bytes INTEGER)")
        if startdate == '' and enddate == '':
            log.info("Inserting tasks without date filtering...")
            for task in tc.endpoint_manager_task_list(num_results=None, filter_endpoint=endpointid):
                log.debug("INSERT INTO People VALUES(\'{}\', {})".format(task["owner_string"],task["bytes_transferred"]))
                cur.execute("INSERT INTO People VALUES(\'{}\', {})".format(task["owner_string"],task["bytes_transferred"]))
        else:
            log.info("Inserting tasks with date filtering...")
            for task in tc.endpoint_manager_task_list(num_results=None, filter_endpoint=endpointid, filter_completion_time="{},{}".format(str(startdate), str(enddate))):
                log.debug("INSERT INTO People VALUES(\'{}\', {})".format(task["owner_string"],task["bytes_transferred"]))
                cur.execute("INSERT INTO People VALUES(\'{}\', {})".format(task["owner_string"],task["bytes_transferred"]))
        log.info("Executing SQL to gather statistics...")
        cur.execute("SELECT Name, count(Name), sum(Bytes) FROM People GROUP BY Name ORDER BY sum(Bytes) DESC")
        print('Jobs\tGigabytes\tUser')
        for row in cur:
            print('{}\t{}\t{}'.format(row[1], str(float(row[2])/1000000000), row[0]))

def job_count(endpointid, startdate, enddate):
    log.info("Aquiring access token from refresh token...")
    tc = auth.authenticate()
    log.info("Running Globus request...")
    count = 0
    if startdate == '' and enddate == '':
        for task in tc.endpoint_manager_task_list(num_results=None, filter_endpoint=endpointid):
            count += 1
    else:
        for task in tc.endpoint_manager_task_list(num_results=None, filter_endpoint=endpointid, filter_completion_time="{},{}".format(str(startdate), str(enddate))):
            count += 1
    print("{}".format(count))


def running_count(endpointid):
    log.info("Aquiring access token from refresh token...")
    tc = auth.authenticate()
    log.info("Running Globus request...")
    count = 0
    for task in tc.endpoint_manager_task_list(num_results=None, filter_endpoint=endpointid, filter_status="ACTIVE"):
        count += 1
    print("{}".format(count))

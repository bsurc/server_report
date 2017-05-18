#!python3
"""Statistics generating functions.

This file contains functions that generate metrics from the globus sdk.

Functions:
list_endpoints -- Return a list of managed endpoints.
user_frequency -- Show users by data transferred and job count.
job_count      -- Show total jobs in date range.
running_count  -- Show jobs currently active.
"""
import sqlite3 as lite
import server_report.auth as auth
import logging

log = logging.getLogger(__name__)


def list_endpoints():
    """Return the list of managed endpoints for the current user."""
    log.info("Aquiring transfer access token from refresh token...")
    tc = auth.authorize_transfer()
    print("My Managed Endpoints:")
    for ep in tc.endpoint_manager_monitored_endpoints():
        print("[{}] {}".format(ep["id"], ep["display_name"]))


def user_frequency(epid, startdate, enddate):
    """Return a list of users on an endpoint sorted by data moved."""
    insertstring = "INSERT INTO People VALUES(\'{}\', {})"
    log.info("Aquiring transfer access token from refresh token...")
    tc = auth.authorize_transfer()
    log.info("Creating database in memory...")
    con = lite.connect(':memory:')
    with con:
        emtl = tc.endpoint_manager_task_list
        cur = con.cursor()
        log.info("Creating Table...")
        cur.execute("CREATE TABLE People(Name TEXT, Bytes INTEGER)")
        if startdate == '' and enddate == '':
            log.info("Inserting tasks without date filtering...")
            for task in emtl(
                    num_results=None, filter_endpoint=epid):
                log.debug(insertstring.format(
                    task["owner_string"], task["bytes_transferred"]))
                cur.execute(insertstring.format(
                    task["owner_string"], task["bytes_transferred"]))
        else:
            log.info("Inserting tasks with date filtering...")
            for task in emtl(num_results=None,
                             filter_endpoint=epid,
                             filter_completion_time="{},{}".format(
                                 str(startdate), str(enddate))):
                log.debug(insertstring.format(task["owner_string"],
                                              task["bytes_transferred"]))
                cur.execute(insertstring.format(task["owner_string"],
                                                task["bytes_transferred"]))
        log.info("Executing SQL to gather statistics...")
        cur.execute("SELECT Name, count(Name), sum(Bytes) "
                    "FROM People GROUP BY Name "
                    "ORDER BY sum(Bytes) DESC")
        print('Jobs\tGigabytes\tUser')
        for row in cur:
            print('{}\t{}\t{}'.format(
                row[1], str(float(row[2])/1000000000), row[0]))


def job_count(endpointid, startdate, enddate):
    """Return the number of jobs that completed in the given time period."""
    log.info("Aquiring transfer access token from refresh token...")
    tc = auth.authorize_transfer()
    log.info("Running Globus request...")
    count = 0
    if startdate == '' and enddate == '':
        for task in tc.endpoint_manager_task_list(
                num_results=None, filter_endpoint=endpointid):
            count += 1
    else:
        for task in tc.endpoint_manager_task_list(
                num_results=None, filter_endpoint=endpointid,
                filter_completion_time="{},{}".format(str(startdate),
                                                      str(enddate))):
            count += 1
    print("{}".format(count))


def running_count(endpointid):
    """Return the number of currently active jobs on an endpoint."""
    log.info("Aquiring transfer access token from refresh token...")
    tc = auth.authorize_transfer()
    log.info("Running Globus request...")
    count = 0
    for task in tc.endpoint_manager_task_list(
            num_results=None, filter_endpoint=endpointid,
            filter_status="ACTIVE"):
        count += 1
    print("{}".format(count))


def errored_jobs(epid, startdate, enddate):
    """Return a list of errors on an endpoint."""
    insertstring = ("INSERT INTO Tasks VALUES(\'{}\', \'{}\', "
                    "\'{}\', \'{}\')")
    log.info("Aquiring transfer access token from refresh token...")
    tc = auth.authorize_transfer()
    log.info("Creating database in memory...")
    con = lite.connect(':memory:')
    with con:
        emtl = tc.endpoint_manager_task_list
        cur = con.cursor()
        log.info("Creating Table...")
        cur.execute("CREATE TABLE Tasks(Name TEXT, TaskID TEXT, Status TEXT, "
                    "NiceStatus TEXT)")
        if startdate == '' and enddate == '':
            log.info("Inserting tasks without date filtering...")
            for task in emtl(
                    num_results=None, filter_endpoint=epid):
                log.debug(insertstring.format(
                    task["owner_string"], task["task_id"],
                    task["status"], task["nice_status"]))
                cur.execute(insertstring.format(
                    task["owner_string"], task["task_id"],
                    task["status"], task["nice_status"]))
        else:
            log.info("Inserting tasks with date filtering...")
            for task in emtl(num_results=None,
                             filter_endpoint=epid,
                             filter_completion_time="{},{}".format(
                                 str(startdate), str(enddate))):
                log.debug(insertstring.format(
                    task["owner_string"], task["task_id"],
                    task["status"], task["nice_status"]))
                cur.execute(insertstring.format(
                    task["owner_string"], task["task_id"],
                    task["status"], task["nice_status"]))
        log.info("Executing SQL to gather statistics...")
        cur.execute("SELECT Name, TaskID, Status, NiceStatus "
                    "FROM Tasks WHERE Status NOT IN "
                    "('SUCCEEDED', 'ACTIVE')")
        for row in cur:
            print('{0}\t{1}\t{2}\t{3}'.format(row[0],row[1],row[2],row[3]))

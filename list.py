#!python3
import globus_sdk
import pickle
import os
from subprocess import call
import sys
import sqlite3 as lite
import server_report.auth

def list(endpointid=None):
    # Initialize Client and Token
    client = globus_sdk.NativeAppAuthClient('cca6968a-cc55-4ee9-a651-b66f059037bf')
    token = server_report.auth.read_token()

    # Get tokens we need
    globus_transfer_data = token.by_resource_server['transfer.api.globus.org']
    transfer_at = globus_transfer_data['access_token']
    transfer_rt = globus_transfer_data['refresh_token']
    transfer_rt_expiry = globus_transfer_data['expires_at_seconds']

    # Validate token and get authorizer
    authorizer = globus_sdk.RefreshTokenAuthorizer(transfer_rt, client, access_token=transfer_at, expires_at=transfer_rt_expiry)
    #
    tc = globus_sdk.TransferClient(authorizer=authorizer)

    if endpointid == None:
        print("My Managed Endpoints:")
        for ep in tc.endpoint_manager_monitored_endpoints():
            print("[{}] {}".format(ep["id"], ep["display_name"]))
    else:
        con = lite.connect(':memory:')
        with con:
            cur = con.cursor()
            cur.execute("CREATE TABLE People(Name TEXT)")
            for task in tc.endpoint_manager_task_list(num_results=None, filter_endpoint=endpointid):
                cur.execute("INSERT INTO People VALUES(\'{}\')".format(task["owner_string"]))
            cur.execute("SELECT Name, count(*) FROM People GROUP BY Name ORDER BY count(*) DESC")
            for row in cur:
                print('{}\t{}'.format(row[1], row[0]))


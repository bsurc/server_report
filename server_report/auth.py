#!python3
"""Authentication library for server_report.

This file contains functions that get and store tokens using the globus sdk.

Functions:
request_token       -- Perform OAuth flow to get token.
read_token          -- Read token from pickle file.
authorize_transfer  -- Get authorizer from token.
"""
from __future__ import unicode_literals
import globus_sdk
import pickle
import os
from prompt_toolkit import prompt
import logging

log = logging.getLogger(__name__)

CLIENT_ID = 'cca6968a-cc55-4ee9-a651-b66f059037bf'
auth_client = globus_sdk.auth.AuthClient(client_id=CLIENT_ID)
directory = '{}/.server_report/'.format(os.environ['HOME'])
tokenfile = '{}/.server_report/token.dat'.format(os.environ['HOME'])

def request_token():
    """Run OAuth flow and store response in pickle for future use."""
    # Create client profile and start OAuth flow
    client = globus_sdk.auth.GlobusNativeAppFlowManager(auth_client, refresh_tokens=True)
    # Request authorization URL and prompt user
    authorize_url = client.get_authorize_url()
    print('Please go to this URL and login: {0}'.format(authorize_url))
    # Get auth code response from user
    auth_code = prompt("Please enter the code you get after login here: ").strip()
    token_response = client.exchange_code_for_tokens(auth_code)
    # Save token to file using pickle, overwriting old creds
    if not os.path.exists(directory):
        os.makedirs(directory)
    if os.path.isfile(tokenfile):
        os.remove(tokenfile)
    fw = open(tokenfile, 'wb')
    pickle.dump(token_response.by_resource_server, fw)
    fw.close()
    os.chmod(tokenfile, 256)
    return


def read_token():
    """Get cached token from pickle file."""
    if not os.path.isfile(tokenfile):
        request_token()
    fd = open(tokenfile, 'rb')
    token_response = globus_sdk.auth.token_response
    token_response.by_resource_server = pickle.load(fd)
    return token_response


def authorize_transfer():
    """Generate authorizer for transfer api use."""
    # Initialize Client and Token
    client = globus_sdk.NativeAppAuthClient(CLIENT_ID)
    token = read_token()
    # Get tokens we need
    globus_transfer_data = token.by_resource_server['transfer.api.globus.org']
    transfer_at = globus_transfer_data['access_token']
    transfer_rt = globus_transfer_data['refresh_token']
    transfer_rt_expiry = globus_transfer_data['expires_at_seconds']
    # Validate token and get authorizer
    auth = globus_sdk.RefreshTokenAuthorizer(
            transfer_rt, client,
            access_token=transfer_at,
            expires_at=transfer_rt_expiry)
    return(globus_sdk.TransferClient(authorizer=auth))

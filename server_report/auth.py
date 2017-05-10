#!python3
import globus_sdk
import pickle
import os
from prompt_toolkit import prompt

CLIENT_ID = 'cca6968a-cc55-4ee9-a651-b66f059037bf'
directory = '{}/.server_report/'.format(os.environ['HOME'])
tokenfile = '{}/.server_report/token.dat'.format(os.environ['HOME'])

def request_token():
    # Create client profile and start OAuth flow
    client = globus_sdk.NativeAppAuthClient(CLIENT_ID)
    # We want refresh tokens for
    client.oauth2_start_flow(refresh_tokens=True)
    # Request authorization URL and prompt user
    authorize_url = client.oauth2_get_authorize_url()
    print('Please go to this URL and login: {0}'.format(authorize_url))
    # Get auth code response from user
    auth_code = prompt(
                'Please enter the code you get after login here: ').strip()
    token_response = client.oauth2_exchange_code_for_tokens(auth_code)
    # Save token to file using pickle, overwriting old creds
    if not os.path.exists(directory):
            os.makedirs(directory)
    if os.path.isfile(tokenfile):
        os.remove(tokenfile)
    fw = open(tokenfile, 'wb')
    pickle.dump(token_response, fw)
    fw.close()
    return

def read_token():
    if not os.path.isfile(tokenfile):
        request_token()
    fd = open(tokenfile, 'rb')
    token_response = pickle.load(fd)
    return token_response

def authenticate():
    # Initialize Client and Token
    client = globus_sdk.NativeAppAuthClient(CLIENT_ID)
    token = read_token()
    # Get tokens we need
    globus_transfer_data = token.by_resource_server['transfer.api.globus.org']
    transfer_at = globus_transfer_data['access_token']
    transfer_rt = globus_transfer_data['refresh_token']
    transfer_rt_expiry = globus_transfer_data['expires_at_seconds']
    # Validate token and get authorizer
    authorizer = globus_sdk.RefreshTokenAuthorizer(transfer_rt, client, access_token=transfer_at, expires_at=transfer_rt_expiry)
    return(globus_sdk.TransferClient(authorizer=authorizer))

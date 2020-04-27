import pickle
import os
import time
from datetime import date, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying scopes, delete file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify'
]

def get_service(cron=0, cred_path="credentials.json", token_path='token.pickle'):
    """ 
        Returns a gmail service object. 

        CLIENT_SECRETS_FILE contains the OAuth 2.0 info for this application.

        token.pickle (TOKEN) stores user's access and refresh tokens, & is created 
        automatically when the authorization flow completes for the first time.
    """
    if cron==1: # Need absolute paths for cron.
        cwd = os.getcwd()
        CLIENT_SECRETS_FILE = cwd + f'/{cred_path}'
        TOKEN = cwd + f'/{token_path}'
    else: # Relative paths.
        CLIENT_SECRETS_FILE = f"{cred_path}"
        TOKEN = f'{token_path}'

    creds = None

    if os.path.exists(TOKEN):
        with open(TOKEN, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN, 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    return service

def read_individual_email(service, user_id, email_id):
    """
    Get a Message with given email_id.

    Args:
        - service (googleapiclient.discovery.Resource): Authorized Gmail API service instance.
        - user_id (str): User's email address. Value "me" is used to use the authenticated user.
        - email_id (str): The ID of the Message required.

    Returns:
        A Message.
    """
    try:
        res = {}

        message = service.users().messages().get(userId=user_id, id=email_id).execute()
        res['message_id'] = email_id
        res['body'] = message['snippet']

        for index, value in enumerate(message['payload']['headers']):
            if value['name'] == 'Date':
                res['date'] = value['value']
            if value['name'] == 'Subject':
                res['subject'] = value['value']
            if value['name'] == 'From':
                res['from'] = value['value']

        mark_read(service, user_id, email_id)

        return res
    except Exception as error:
        print(f'FUNC::read_individual_email -> {error}')
        return None

def mark_read(service, user_id, email_id):
    ''' Removes UNREAD lable from message. '''
    service.users().messages().modify(userId=user_id, id=email_id, body={'removeLabelIds': ['UNREAD']}).execute()


def get_all_emails(service, user_id='me', query_str='', label_ids=['INBOX'], includeSpamTrash=False):
    """
    Gets all messages.

    Args:
        - service (googleapiclient.discovery.Resource): Authorized Gmail API service instance.
        - user_id (str): User's email address. Value "me" is used to use the authenticated user.
        - query_str (str): Filters for the query.
        - label_ids (list of str): Only return Messages with these labelIds applied.
        - includeSpamTrash (bool): Include messages from SPAM and TRASH in the results.

    Returns:
        A list of all messages.
    """
    try:
        # Call the Gmail API
        response = service.users().messages().list(userId=user_id, q=query_str, labelIds=label_ids).execute()
        emails = []

        if 'messages' in response:
            emails.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query_str, labelIds=label_ids, pageToken=page_token).execute()
            emails.extend(response['messages'])

        return emails
    except Exception as error:
        print(f'FUNC::get_all_emails -> {error}')
        return None

def get_gmail_query_filter(days_into_past=1, read_status='unread'):
    emails_after_this_date = date.today() - timedelta(days_into_past)
    unixtime = int(time.mktime(emails_after_this_date.timetuple()))
    return f'is:{read_status} after:{unixtime}'


# cd/usr/bin/
# sudo yum install python37
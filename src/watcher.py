''' This script is run by a cron job '''
import gmail
import json
import os
import requests
from datetime import datetime

service = gmail.get_service(cron=1)

def get_emails():
    ''' Will get all emails which pass filter. '''
    try:
        q_str = gmail.get_gmail_query_filter(days_into_past=30)
        emails = gmail.get_all_emails(service=service, user_id='me', query_str=q_str)
        
        log(emails)
        return emails
    except (Exception) as error:
        print(f"get_emails::error --> {error}")

def read_emails(email_list: list):
    ''' Will extract email data. '''
    try:
        all_email = {}

        for index, value in enumerate(email_list):
            email_data = gmail.read_individual_email(service=service, user_id='me', email_id=value['id'])
            all_email[str(index)] = email_data

        log(all_email)
        return all_email
    except (Exception) as error:
        print(f"read_emails::error --> {error}")

def post_leads(url=None, data={}):
    ''' Will post all extracted leads. '''
    try:
        res = requests.post(url=url, data=data)

        print(f'Accessed on: {str(datetime.now())}\n{res}\n')
        return res
    except (Exception) as error:
        print(f"post_leads::error --> {error}")

def log(data):
    print(f'Accessed on: {str(datetime.now())}\n{json.dumps(data)}\n')

emails = get_emails()
all_emails = read_emails(emails)
post_leads(url=None, data=all_emails)
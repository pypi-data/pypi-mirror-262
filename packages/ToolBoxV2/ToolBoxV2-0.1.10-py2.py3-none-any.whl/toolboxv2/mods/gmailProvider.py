import os
import pickle
# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

from toolboxv2 import get_app

# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ['https://mail.google.com/']
user_email = 'your_gmail@gmail.com'

Name = 'gmailProvider'
export = get_app("gmailProvider.Export").tb
version = '0.0.1'
default_export = export(mod_name=Name, test=False, state=False, version=version, level=2)


@default_export
def gmail_authenticate(name='main'):
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists(f"token-{name}.pickle"):
        with open(f"token-{name}.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(os.getenv("GOOGLE_CREDENTIALS_FILE"), SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open(f"token-{name}.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)


# service_ = gmail_authenticate()


# Adds the attachment with the given filename to the given message
def add_attachment(message, filename):
    content_type, encoding = guess_mime_type(filename)
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(filename, 'rb')
        msg = MIMEText(fp.read().decode(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(filename, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(filename, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(filename, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(filename)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)


def build_message(destination, obj, body, attachments=None):
    if attachments is None:
        attachments = []
    if not attachments:  # no attachments given
        message = MIMEText(body)
        message['to'] = destination
        message['from'] = user_email
        message['subject'] = obj
    else:
        message = MIMEMultipart()
        message['to'] = destination
        message['from'] = user_email
        message['subject'] = obj
        message.attach(MIMEText(body))
        for filename in attachments:
            add_attachment(message, filename)
    return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}


@default_export
def send_message(service, destination, obj, body, attachments=None):
    if attachments is None:
        attachments = []
    return service.users().messages().send(
        userId="me",
        body=build_message(destination, obj, body, attachments)
    ).execute()


@default_export
def search_messages(service, query):
    result = service.users().messages().list(userId='me', q=query).execute()
    messages = []
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages


# utility functions
def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)


def parse_parts(service, parts, folder_name, message):
    """
    Utility function that parses the content of an email partition
    """
    row_data = ""
    if parts:
        for part in parts:
            filename = part.get("filename")
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = body.get("data")
            file_size = body.get("size")
            part_headers = part.get("headers")
            if part.get("parts"):
                # recursively call this function when we see that a part
                # has parts inside
                parse_parts(service, part.get("parts"), folder_name, message)
            if mimeType == "text/plain":
                # if the email part is text plain
                if data:
                    text = urlsafe_b64decode(data).decode()
                    row_data += text + "\n"
    return row_data


@default_export
def read_message(service, message):
    """
    This function takes Gmail API `service` and the given `message_id` and does the following:
        - Downloads the content of the email
        - Prints email basic information (To, From, Subject & Date) and plain/text parts
        - Creates a folder for each email based on the subject
        - Downloads text/html content (if available) and saves it under the folder created as index.html
        - Downloads any file that is attached to the email and saves it in the folder created
    """
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    # parts can be the message body, or attachments
    payload = msg['payload']
    headers = payload.get("headers")
    parts = payload.get("parts")
    folder_name = "email"
    has_subject = False
    final_msg = ""
    if headers:
        # this section prints email basic info & creates a folder for the email
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'from':
                # we print the From address
                print("From:", value)
                final_msg += f"From: {value}\n"
            if name.lower() == "to":
                # we print the To address
                # final_msg += f"To: {value}"
                print("To:", value)
            if name.lower() == "subject":
                # make our boolean True, the email has "subject"
                has_subject = True
                # make a directory with the name of the subject
                folder_name = clean(value)
                # we will also handle emails with the same subject name
                final_msg += f"Subject: {value}\n"
                print("Subject:", value)
            if name.lower() == "date":
                # we print the date when the message was sent
                final_msg += f"Date: {value}\n"
                print("Date:", value)
    final_msg += parse_parts(service, parts, folder_name, message)
    print("=" * 50)
    return final_msg


@default_export
def mark_as_read(service, query):
    messages_to_mark = search_messages(service, query)
    print(f"Matched emails: {len(messages_to_mark)}")
    return service.users().messages().batchModify(
        userId='me',
        body={
            'ids': [msg['id'] for msg in messages_to_mark],
            'removeLabelIds': ['UNREAD']
        }
    ).execute()


@default_export
def delete_messages(service, query):
    messages_to_delete = search_messages(service, query)
    # it's possible to delete a single message with the delete API, like this:
    # service.users().messages().delete(userId='me', id=msg['id'])
    # but it's also possible to delete all the selected messages with one query, batchDelete
    return service.users().messages().batchDelete(
        userId='me',
        body={
            'ids': [msg['id'] for msg in messages_to_delete]
        }
    ).execute()


# get emails that match the query you specify
# results = search_messages(service, "Python Code")
# print(f"Found {len(results)} results.")
# # for each email matched, read it (output plain/text to console & save HTML and attachments)
# for msg in results:
#     read_message(service, msg)
# Example
# test send email
# send_message(service, "destination@domain.com", "This is a subject",
#             "This is the body of the email", ["test.txt", "anyfile.png"])

# get the Gmail API service


import imaplib
import email
from email.header import decode_header
import os


# account credentials
# use your email provider's IMAP server, you can look for your provider's IMAP server on Google
# or check this page: https://www.systoolsgroup.com/imap/
# for office 365, it's this:
@default_export
def log_in(username, password, imap_server="outlook.office365.com"):
    imap = imaplib.IMAP4_SSL(imap_server)
    # authenticate
    imap.login(username, password)
    return imap


@default_export
def get_msg(imap, N=3):
    status, messages = imap.select("INBOX")
    # number of top emails to fetch
    # total number of emails
    messages = int(messages[0])
    ret_messages = []
    for i in range(messages, messages - N, -1):
        # fetch the email message by ID
        res, msg = imap.fetch(str(i), "(RFC822)")
        ret_message = ""
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                # decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                print("Subject:", subject)
                ret_message += f"Subject:{subject}\n"
                ret_message += f"From:{From}"
                print("From:", From)
                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            # print text/plain emails and skip attachments
                            ret_message += f"Body:\n{body}"
                            print(body)
                        elif "attachment" in content_disposition:
                            # download attachment
                            filename = part.get_filename()
                            if filename:
                                folder_name = clean(subject)
                                ret_message += f"\nFile:{folder_name}\n"
                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    # get the email body
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        # print only text email parts
                        ret_message += f"Body:\n{body}"
                        print(body)
                if content_type == "text/html":
                    folder_name = clean(subject)
                    ret_message += f"\nFile:{folder_name}\n"
                print("=" * 100)
                ret_messages.append(ret_message)
    return ret_messages


@default_export
def log_lout(imap):
    # close the connection and logout
    imap.close()
    imap.logout()

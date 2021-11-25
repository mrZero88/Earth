import imaplib
import email
import os
import sys
import threading
import time
import uuid
from dateutil import parser
from email.header import decode_header
from gi.repository import GObject

from filters.email_filter import EmailFilter
from models.email import Email


class EmailService:
    PROJECT_ROOT = sys.path[1]
    emails = []

    on_email_load = None
    on_email_insert = None

    def __init__(self, account, on_email_load, on_email_insert):
        self.account = account
        self.imap = imaplib.IMAP4_SSL(account.imap)
        self.on_email_load = on_email_load
        self.on_email_insert = on_email_insert

    def login(self, user_name, password):
        self.imap.login(user_name, password)

    def read_emails(self, mailbox, number_of_emails_to_read):
        thread = threading.Thread(target=self.read_emails_async, args=(mailbox, number_of_emails_to_read))
        thread.daemon = True
        thread.start()

    def read_emails_async(self, mailbox, number_of_emails_to_read):
        if not self.on_email_load:
            self.on_email_load = lambda r, e: None

        error = None
        try:

            status, messages = self.imap.select(mailbox)
            # number of top emails to fetch
            n = number_of_emails_to_read
            # total number of emails
            messages = int(messages[0])

            for i in range(messages, messages - n, -1):

                content_type = ""
                email_from = ""
                email_subject = ""
                email_text = ""
                email_body = ""
                email_date = ""
                email_file_path = ""

                # fetch the email message by ID
                res, msg = self.imap.fetch(str(i), "(RFC822)")
                for response in msg:
                    if isinstance(response, tuple):
                        # parse a bytes email into a message object
                        msg = email.message_from_bytes(response[1])
                        # decode the email subject
                        email_subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(email_subject, bytes):
                            # if it's a bytes, decode to str
                            if encoding is not None:
                                email_subject = email_subject.decode(encoding)
                            else:
                                email_subject = email_subject.decode()
                        # decode email sender
                        email_from, encoding = decode_header(msg.get("From"))[0]
                        if isinstance(email_from, bytes):
                            if encoding is not None:
                                email_from = email_from.decode(encoding)
                            else:
                                email_from = email_from.decode()

                        email_date, encoding = decode_header(msg.get("Date"))[0]
                        if isinstance(email_date, bytes):
                            email_date = email_date.decode(encoding)

                        email_date = parser.parse(email_date).timestamp()

                        # if the email message is multipart
                        if msg.is_multipart():
                            # iterate over email parts
                            for part in msg.walk():
                                # extract content type of email
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))
                                try:
                                    payload = part.get_payload(decode=True)
                                    # get the email email_body
                                    email_body = payload.decode("unicode_escape")

                                except:
                                    pass
                                # if content_type == "text/plain" and "attachment" not in content_disposition:
                                # print text/plain emails and skip attachments
                                # print(email_body)
                                if "attachment" in content_disposition:
                                    # download attachment
                                    filename = part.get_filename()
                                    if filename:
                                        if content_type == "text/html":
                                            email_file_path = self.create_file_with_html(email_body, filename)
                        else:
                            # extract content type of email
                            content_type = msg.get_content_type()
                            # get the email email_body
                            payload = msg.get_payload(decode=True)
                            email_body = payload.decode()
                            if email_body == "":
                                email_body = payload

                        if content_type == "text/html":
                            email_file_path = self.create_file_with_html(email_body, "index.html")
                        elif content_type == "text/plain":
                            email_text = email_body

                email_obj = Email(id=None, account_id=self.account.id,
                                  email_from=EmailFilter.filter_email_from(email_from),
                                  to=self.account.email,
                                  cc=None, from_name=EmailFilter.filter_name(email_from),
                                  subject=EmailFilter.filter_subject(email_subject),
                                  text=email_text,
                                  file_path=email_file_path,
                                  date=email_date)
                self.emails.append(email_obj)
                GObject.idle_add(lambda: self.on_email_load(email_obj, error))
                GObject.idle_add(lambda: self.on_email_insert(email_obj, error))
                time.sleep(0.05)
        except Exception as err:
            error = err
            print(err)
            self.imap.close()
            self.imap.logout()
        # close the connection and logout
        self.imap.close()
        self.imap.logout()

    def create_file_with_html(self, email_body, file_name):
        email_uuid = uuid.uuid1()
        folder_name = self.clean(str(email_uuid))
        folder_full_path = EmailService.PROJECT_ROOT + "/emails/" + str(
            self.account.id) + "/" + folder_name
        if not os.path.isdir(folder_full_path):
            # make a folder for this email (named after the subject)
            os.mkdir(folder_full_path)
        email_file_path = os.path.join(folder_full_path, file_name)
        # write the file
        open(email_file_path, "w").write(email_body)
        return email_file_path

    def get_emails(self):
        return self.emails

    def clean(self, text):
        # clean text for creating a folder
        return "".join(c if c.isalnum() else "_" for c in text)

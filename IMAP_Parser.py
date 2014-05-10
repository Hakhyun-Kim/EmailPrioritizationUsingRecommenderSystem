#!/usr/bin/python

import imaplib
import sys
import email
import re

#FOLDER=sys.argv[1]
FOLDER='Inbox'
LOGIN='your name@sunykorea.ac.kr'
PASSWORD='your password'
IMAP_HOST = 'imap.gmail.com'  # Change this according to your provider

email_list = []
email_unique = []

mail = imaplib.IMAP4_SSL(IMAP_HOST)
mail.login(LOGIN, PASSWORD)
mail.select(FOLDER) 

result, data = mail.search(None, 'ALL')
ids = data[0]
id_list = ids.split()
for i in id_list:
	typ, data = mail.fetch(i,'(RFC822)')
	for response_part in data:
		if isinstance(response_part, tuple):
			msg = email.message_from_string(response_part[1])
			sender = msg['from'].split()[-1]
			address = re.sub(r'[<>]','',sender)
# Ignore any occurences of own email address and add to list
	if not re.search(r'' + re.escape(LOGIN),address) and not address in email_list:
		email_list.append(address)
		print address
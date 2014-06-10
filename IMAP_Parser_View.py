#!/usr/bin/python

import imaplib
import sys
import email
import re

def knearest(sendcount, receivercount):
		#ratio normailze : 8:2(4:1)
		v = 5.0 / (sendcount + receivercount)
		sendcount = sendcount*v
		receivercount = receivercount*v
		return (sendcount-4)*(sendcount-4)+(receivercount-1)*(receivercount-1);

from collections import defaultdict

#FOLDER=sys.argv[1]
FOLDER='Inbox'
LOGINDATA = {'hakhyun.kim@sunykorea.ac.kr','hakhyun.kim@stonybrook.edu'}
PASSWORD='password'
IMAP_HOST = 'imap.gmail.com'

email_senderDict = defaultdict(int)
email_receiverDict = defaultdict(int)
email_unique = []


for LOGIN in LOGINDATA:
	
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
				
				if(type(msg['from']) != type(None)):
					sender = msg['from'].split()[-1]
				if(type(msg['to']) != type(None)):
					receiver = msg['to'].split()[-1]
					sender_address = re.sub(r'[<>]','',sender)
					receiver_address = re.sub(r'[<>]','',receiver)
			
		if sender_address in email_senderDict:
			email_senderDict[sender_address] += 1
		else:
			email_senderDict[sender_address] = 1

		if receiver_address in email_receiverDict:
			email_receiverDict[receiver_address] += 1
		else:
			email_receiverDict[receiver_address] = 1


	print 'match list'
	
	for key, value in email_senderDict.iteritems():
		if key in email_receiverDict:
			print key,'send count', value, 'receive count', email_receiverDict[key],'nearest point:', knearest(value,email_receiverDict[key])

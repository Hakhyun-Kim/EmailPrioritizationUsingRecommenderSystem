#!/usr/bin/python

import imaplib
import sys
import email
import re

#sample important email : Professor Lee. 


def knearest(sendcount, receivercount):
		return (sendcount-9)*(sendcount-9)+(receivercount-3)(receivercount-3);

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
			
		#print 'sender: ' + sender_address
		#print 'receiver: ' + receiver_address 

		if sender_address in email_senderDict:
			email_senderDict[sender_address] += 1
		else:
			email_senderDict[sender_address] = 1

		if receiver_address in email_receiverDict:
			email_receiverDict[receiver_address] += 1
		else:
			email_receiverDict[receiver_address] = 1

	#mail.close()
	#mail.shutdown()
	#print 'sender list'
	#for key, value in email_senderDict.iteritems():
	#	print 'to', key, value, 'emails sent'

	#print 'receiver list'
	#for key, value in email_receiverDict.iteritems():
	#	print 'from', key, value, 'emails received'

	print 'match list'

	for key, value in email_senderDict.iteritems():
		if key in email_receiverDict:
			if ( knearest(value,email_receiverDict[key]) > 5 ):
				print' Would like to add','key', 'address to be your important email address?'
			print key,'send count', value, 'receive count', email_receiverDict[key],'nearest point:', knearest(key,value)

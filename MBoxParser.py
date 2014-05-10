print('Hello World')

import mailbox

def print_payload(message):
  # if the message is multipart, its payload is a list of messages
  if message.is_multipart():
    for part in message.get_payload(): 
      print_payload(part)
  else:
    print message.get_payload(decode=True)
    
mbox = mailbox.mbox('export.mbox')
for message in mbox:
  print message['subject']
  print_payload(message)
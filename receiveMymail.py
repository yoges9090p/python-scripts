import pyzmail
import sys
from email_data import *
import imapclient
data = sys.argv

# step-1 Making a request to IMAPClient to make conection
with imapclient.IMAPClient('imap.gmail.com', ssl=True) as imapObj:
    # step-2 loging in the imap server
    imapObj.login(MYMAIL, MYPASS)

    # #printing the list of folders in gmail
    # import pprint

    # pprint.pprint(imapObj.list_folders())

    # step-3 selecting a folder from the above list, (readonly = True) will help us prevent from making changes to
    # our mails
    imapObj.select_folder('INBOX', readonly=False)

    # step-4 Now that the folder is selected, we can finally search for mails, and we store it in UIDs
    UIDs = imapObj.search([data[1], data[2]])

    #here we fetch body of messages using UIDs, but it's not in readable format
    rawMessages = imapObj.fetch(UIDs, ['BODY[]'])
    #finding the keys from rawmessages and then store it as a list
    item_list = list(rawMessages.keys())
    for item in item_list:
        message = pyzmail.PyzMessage.factory(rawMessages[item][b'BODY[]'])
        file_name = message.text_part.get_payload().decode(message.text_part.charset).strip("\r\n")
        attachment = message.get_payload()[1]
        # if(message.text_part != None):
        #     print(message.text_part.get_payload().decode(message.text_part.charset))
        # if(message.html_part != None):
        #     print(message.html_part.get_payload().decode(message.html_part.charset))
        if len(file_name)<30:
            with open(file_name, "wb") as myfile:
                    myfile.write(attachment.get_payload(decode=True))
    if len(file_name)<30:
        imapObj.delete_messages(UIDs)
        imapObj.expunge()

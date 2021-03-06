from solver import *
import time
import poplib
import imaplib
import email

def readUserFile():
    try:
        with open('login.txt', 'r') as file:
            return file.readline()[:-1]
    except:
        raise Exception("Can't find login file!")

def readPassFile():
    try:
        with open('login.txt', 'r') as file:
            return file.readlines()[1]
    except:
        raise Exception("Can't read/find login file!")

def readSendFile():
    try:
        with open('send.txt', 'r') as file:
            return file.readline()
    except:
        raise Exception("Can't find send file!")

gmail_user = readUserFile()
gmail_pwd = readPassFile()
import smtplib
def send_email(subject, body, to = readSendFile()):
    FROM = readUserFile()
    TO = [to]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(FROM, TO, message)
    server.close()
    print('Succesfully sent mail!')

def sendSolution(puzzle, add = None):
    subj = 'Solution to the puzzle!'
    body = '[Original puzzle]\n' + formatNicely(datfromtext(puzzle))+ '\n\n' +\
        '[Solution]\n'
    try:
        body += formatNicely(solve(datfromtext(puzzle)))
    except:
        body += 'ERROR finding solution!!'
    if add is None:
        send_email(subj,body)
    else:
        send_email(subj,body,to=add)

if __name__ == '__main__':
    while(True):
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(gmail_user, gmail_pwd)
        mail.select('inbox')
        result, data = mail.search(None, 'UnSeen', 'HEADER Subject "solve"')
        ids = data[0]
        for num in data[0].split():
            mail.store(num,'+FLAGS','\\Seen')
        id_list = ids.split()
        data = [mail.fetch(id_list[i], "(RFC822)")[1] for i in range(len(id_list))]
        raw_emails = [a[0][1] for a in data]
        messages = [email.message_from_bytes(r) for r in raw_emails]
        # Parse message intom an email object:
        # messages = [email.message_from_bytes(mssg) for mssg in messages]
        for message in messages:
            subj = str(message['subject'])
            if 'solve' in subj.lower():
                # We've gotta solve this puzzle!
                # First, we have to find out who to send it back to
                rAd = str(message['from']).split('<')[1][:-1]
                # Now, we have to get the puzzle they sent
                # So we need to check for the text of the mail
                puz = None
                for part in message.walk():
                    if part.get_content_type() == 'text/plain':
                        puz = str(part.get_payload())
                if puz is None:
                    raise Exception('No text in message!!')
                print((puz,rAd))
                sendSolution(puz, rAd)
        # pop_conn.quit()
        time.sleep(15)
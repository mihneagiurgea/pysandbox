import imaplib
import email

USERNAME = 'skipy3@gmail.com'
PASSWORD = '-----'


def extract_body(payload):
    if isinstance(payload, str):
        return payload
    else:
        strarr = [extract_body(part.get_payload()) for part in payload]
        return '\n'.join(strarr)


def read_gmail():
    conn = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    conn.login(USERNAME, PASSWORD)
    conn.select()
    typ, data = conn.search(None, 'UNSEEN')
    try:
        for num in data[0].split():
            typ, msg_data = conn.fetch(num, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    yield msg
            # typ, response = conn.store(num, '+FLAGS', r'(\Seen)')
    finally:
        try:
            conn.close()
        except:
            pass
        conn.logout()


if __name__ == '__main__':
    read_gmail()

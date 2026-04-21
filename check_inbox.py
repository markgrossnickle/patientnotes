"""Check Gmail inbox for unread patient note emails and return them."""
import json
import base64
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_FILE = '/Users/Shared/Projects/patientnotes/token.json'
CREDS_FILE = '/Users/Shared/Projects/patientnotes/client_secret_554866609662-i3ol846vlfibbc23ovmtmp7aj77bhkb7.apps.googleusercontent.com.json'

# Only process emails from these senders
ALLOWED_SENDERS = ['elizabeth.huser@gmail.com']

# Ignore emails from these senders
IGNORE_SENDERS = ['google.com', 'googleplay', 'accounts.google.com']

def refresh_creds():
    """Load and refresh credentials if needed."""
    creds = Credentials.from_authorized_user_file(TOKEN_FILE)
    if creds.expired and creds.refresh_token:
        from google.auth.transport.requests import Request
        creds.refresh(Request())
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())
    return creds

def check_inbox():
    """Return list of unread emails (excluding Google system emails)."""
    creds = refresh_creds()
    service = build('gmail', 'v1', credentials=creds)

    results = service.users().messages().list(
        userId='me', maxResults=10, q='is:unread'
    ).execute()

    messages = results.get('messages', [])
    emails = []

    for msg in messages:
        m = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        headers = {h['name']: h['value'] for h in m['payload']['headers']}

        from_addr = headers.get('From', '')
        subject = headers.get('Subject', '')

        # Skip unless from an allowed sender
        if not any(allowed in from_addr.lower() for allowed in ALLOWED_SENDERS):
            continue

        # Get body
        payload = m['payload']
        body = ''
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain' and part.get('body', {}).get('data'):
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    break
        elif payload.get('body', {}).get('data'):
            body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')

        # Determine if this is a reply (feedback) or new note
        # Replies have "Re:" in subject or multiple messages in thread
        is_reply = subject.lower().startswith('re:')

        emails.append({
            'id': msg['id'],
            'thread_id': m['threadId'],
            'from': from_addr,
            'subject': subject,
            'message_id': headers.get('Message-ID', ''),
            'body': body,
            'is_feedback': is_reply
        })

    return emails

def send_reply(thread_id, message_id, to_addr, subject, body_text):
    """Send a reply email."""
    from email.mime.text import MIMEText

    creds = refresh_creds()
    service = build('gmail', 'v1', credentials=creds)

    reply = MIMEText(body_text)
    reply['to'] = to_addr
    reply['subject'] = f'Re: {subject}' if not subject.startswith('Re:') else subject
    if message_id:
        reply['In-Reply-To'] = message_id
        reply['References'] = message_id

    raw = base64.urlsafe_b64encode(reply.as_bytes()).decode()
    body = {'raw': raw, 'threadId': thread_id}

    sent = service.users().messages().send(userId='me', body=body).execute()
    return sent['id']

if __name__ == '__main__':
    emails = check_inbox()
    print(json.dumps(emails, indent=2))

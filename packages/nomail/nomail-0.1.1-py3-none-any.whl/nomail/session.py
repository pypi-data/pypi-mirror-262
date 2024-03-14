from typing import Optional

from src.adapter import EmailImapAdapter
from src.email_filter import EmailFilter
from src.email import EmailList
from src.action import Action

def run(action: Action, filter: EmailFilter, rate_limit: int=1) -> EmailList:
    _imap: EmailImapAdapter = EmailImapAdapter()
    emails = _imap.apply(filter, rate_limit)
    act(emails, action)
    return emails

def act(emails, action):
    for email in emails[::-1]:
        action.act(email)

import re
from email.header import decode_header

from dateutil import parser


def format_email(raw_email):
    if not raw_email:
        return None
    if '<' in raw_email:
        return re.split('<|>', raw_email)[1]
    return raw_email


def format_date(date_str):
    return parser.parse(date_str)


def format_subject(raw_subject):
    subject = decode_header(raw_subject)[0][0]
    if isinstance(subject, bytes):
        return decode_bytes(subject)
    return subject


def decode_bytes(subject):
    try:
        return subject.decode()
    except UnicodeDecodeError:
        return subject.decode('unicode_escape')


def format_uid(uid_str):
    return int(uid_str)

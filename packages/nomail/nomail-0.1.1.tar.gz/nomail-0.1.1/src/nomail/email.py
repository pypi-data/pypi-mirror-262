from typing import List
from dataclasses import dataclass, field

import pandas as pd

from src import sanitize
from src import descriptor


class Email:

    # uid = descriptor.Descriptor()

    def __init__(self, msg_data, uid):
        self.recipient = sanitize.format_email(msg_data['To'])
        self.sender = sanitize.format_email(msg_data['From'])
        self.subject = sanitize.format_subject(msg_data['Subject'])
        self.date = sanitize.format_date(msg_data['Date'])
        self.uid = sanitize.format_uid(uid)

    def __repr__(self):
        return " \n".join([str(item) for item in self.__dict__.values()])

    def __iter__(self):
        yield self.subject, self.sender

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.__dict__ == other.__dict__


@dataclass
class EmailList:
    emails: List[Email] = field(default_factory=list)

    def __init__(self, emails):
        self.emails = list(emails)

    def __iter__(self):
        for email in self.emails:
            yield email

    def __getitem__(self, index):
        return self.emails[index]

    def __len__(self):
        return len(self.emails)

    def to_df(self):
        return pd.DataFrame(self.emails)
 
    def limit(self, rate_limit):
        return EmailList(self[:rate_limit])
 
    def filter(self, email_filter):
        return EmailList(email for email in self.emails if email_filter.test(email))

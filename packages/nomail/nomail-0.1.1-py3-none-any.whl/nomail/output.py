from datetime import datetime
import re
import pandas as pd

from src import email


def generate_file_name():
    return 'logs/' + re.sub('[ ]', '_', str(datetime.today()))

def generate_csv_name():
    return generate_file_name() + '.csv'

def generate_html_name():
    return generate_file_name() + '.html'

def write_emails_to_csv(emails: email.EmailList) -> None:
    write_df_to_csv(emails.to_df())


def write_df_to_csv(df: pd.DataFrame) -> None:
    df.to_csv(generate_file_name(), index=False)


def write_emails_to_html(emails: email.EmailList) -> None:
    write_df_to_html(emails.to_df())


def write_df_to_html(df: pd.DataFrame) -> None:
    df.to_html(generate_file_name(), index=False)

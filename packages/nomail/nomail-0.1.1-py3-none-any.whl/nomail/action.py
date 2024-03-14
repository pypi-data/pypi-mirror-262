from abc import ABC, abstractmethod

from src.adapter import EmailImapAdapter


class Action(ABC):

    def __init__(self):
        self._imap = EmailImapAdapter()

    @abstractmethod
    def act(self, email):
        pass


class ActionDelete(Action):

    def act(self, email):
        self._imap.delete_msg(email)


class ActionCopy(Action):

    def act(self, email):
        self._imap.copy_msg(email)


class ActionPrint(Action):

    def act(self, email):
        print(email.sender)


class ActionMove(Action):

    def act(self, email):
        self._imap.copy_msg(email)
        self._imap.delete_msg(email)


class ActionNone(Action):

    def act(self, email):
        pass

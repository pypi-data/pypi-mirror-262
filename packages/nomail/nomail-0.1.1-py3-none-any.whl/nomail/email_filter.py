from abc import ABC, abstractmethod


class EmailFilter(ABC):
    """Filter emails"""

    @abstractmethod
    def test(self, email):
        pass


class EmailFilterNone(EmailFilter):
    """no filtering"""

    def test(self, email):
        return True


class EmailFilterAll(EmailFilter):
    """filter all emails"""

    def test(self, email):
        return False


class EmailFilterList(EmailFilter):
    """filter senders not in list"""

    def __init__(self, address_list):
        self._address_list = address_list

    def test(self, email):
        return email.sender in self._address_list

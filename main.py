import numbers
from datetime import timedelta, datetime
import itertools


class TimeZone:
    def __init__(self, name, offset_hours, offset_minutes):
        if name is None or len(str(name).strip()) == 0:
            raise ValueError("Timezone name cannot be empty.")

        self._name = str(name).strip()

        if not isinstance(offset_hours, numbers.Integral):
            raise ValueError("Hour offset must be an integral.")

        if not isinstance(offset_minutes, numbers.Integral):
            raise ValueError("Minute offset must be an integral.")

        if offset_minutes > 59 or offset_minutes < -59:
            raise ValueError("Minutes offset must be in range (-59,59.")

        offset = timedelta(hours=offset_hours, minutes=offset_minutes)

        if offset > timedelta(hours=14, minutes=0) or offset < timedelta(hours=-12, minutes=0):
            raise ValueError(" Offset must be between -12:00 - +14:00.")

        self._offset_hours = offset_hours
        self._offset_minutes = offset_minutes
        self._offset = offset

    @property
    def offset(self):
        return self._offset

    @property
    def name(self):
        return self._name

    def __eq__(self, other):
        return (isinstance(other, TimeZone) and
                self.name == other.name and
                self.offset == other.offset)

    def __repr__(self):
        return (f"TimeZone(name='{self.name}', "
                f"offset_hours = {self._offset_hours}, "
                f"offset_minutes={self._offset_minutes}).")


class Account:
    transaction_counter = itertools.count(100)
    _interest_rate = 0.05

    _transaction_codes= {
        'deposit': 'D',
        'withdraw': 'W',
        'interest': 'I',
        'rejected': 'X'
    }

    @classmethod
    def get_interest_rate(cls):
        return cls._interest_rate

    @classmethod
    def set_interest_rate(cls, value):
        if not isinstance(value, numbers.Real):
            raise ValueError("Interest rate must be a real number")
        if value < 0:
            raise ValueError("Interest rate must be positive. ")
        cls._interest_rate = value

    def __init__(self, account_number:int, first_name:str, last_name:str ,  initial_balance=0, timezone=None):

        self._account_number = account_number
        self.first_name = first_name
        self.last_name = last_name

        self._balance = float(initial_balance)


        if timezone is None:
            timezone = TimeZone('UTC', 0, 0)
            self.timezone = timezone


    @property
    def balance(self):
        return self._balance

    @property
    def account_number(self):
        return self._account_number

    @property
    def first_name(self):
        return self._name

    @first_name.setter
    def first_name(self, name):
        self.validate_and_set_name(attr_name='_first_name', value=name, filed_name="First name")

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        self.validate_and_set_name(attr_name='_last_name', value=last_name, filed_name="Last name")

    @property
    def timezone(self):
        return self._timezone

    @timezone.setter
    def timezone(self, value):
        if not isinstance(value, TimeZone):
            raise ValueError("Timezone must be a valid an Timezone object")
        self._timezone = value

    def validate_and_set_name(self, attr_name, value, filed_name):
        if value is None or len(str(value).strip()) == 0:
            raise ValueError(f"{filed_name} can not be empty")
        setattr(self, attr_name, str(value).strip())

    def make_transaction(self):
        new_transaction_id = next(Account.transaction_counter)
        return new_transaction_id


# -----------------------------------------------------------------------------------------------------------------------

try:
    a1 = Account(124, "dom", "koz")
    print(a1.__dict__)
except ValueError as ex:
    print(ex)
print(Account.__dict__)
print("---------------------------")
print(a1.__dict__)


try:
    a1.balance = 23
except AttributeError as ex:
    print(ex)


# dt = datetime.utcnow()
# print(dt)
#
# tz1 = TimeZone('BER', -2, -15)
# print(dt + tz1.offset)
#
#
# try:
#     tz = TimeZone('  s ',42,5)
# except ValueError as ex:
#     print(ex)

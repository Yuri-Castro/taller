import re
import uuid
from typing import Any, Callable, List, NoReturn, Optional, Union

from exceptions import (
    BalanceException,
    CreditCardException,
    PaymentException,
    UsernameException,
)


class UserAddEvent:
    def __init__(self, actor, target):
        self.id = str(uuid.uuid4())
        self.actor = actor
        self.target = target


class Payment:

    def __init__(self, amount, actor, target, note):
        self.id = str(uuid.uuid4())
        self.amount = float(amount)
        self.actor = actor
        self.target = target
        self.note = note


Activity = Union[Payment, UserAddEvent]


class User:

    def __init__(
        self,
        username: str,
        useradd_event_callback: Optional[Callable[[Any], Any]] = None,
    ):
        self.credit_card_number: Optional[str] = None
        self.balance: float = 0.0
        self.activities = []
        self.friends: List["User"] = []
        self.useradd_event_callback: Optional[Callable[[Any], Any]] = (
            useradd_event_callback
        )

        if self._is_valid_username(username):
            self.username = username
        else:
            raise UsernameException("Username not valid.")

    def add_friend(self, new_friend: "User"):
        friendadd_event = UserAddEvent(actor=self, target=new_friend)
        self.friends.append(new_friend)
        self.register_activity(friendadd_event)

        if self.useradd_event_callback:
            self.useradd_event_callback([friendadd_event])

    def add_to_balance(self, amount: float):
        self.balance += float(amount)

    def remove_from_balance(self, amount: float) -> NoReturn:
        self.balance -= float(amount)

    def add_credit_card(self, credit_card_number: str):
        if self.credit_card_number is not None:
            raise CreditCardException("Only one credit card per user!")

        if self._is_valid_credit_card(credit_card_number):
            self.credit_card_number = credit_card_number

        else:
            raise CreditCardException("Invalid credit card number.")

    def pay(self, target: "User", amount: float, note: str):
        payment = None
        if self.balance < amount:
            payment = self.pay_with_card(target, amount, note)
        else:
            payment = self.pay_with_balance(target, amount, note)
        if payment:
            self.register_activity(payment)

    def register_activity(
        self, activities: Union[Activity, List[Activity]]
    ) -> NoReturn:
        if not isinstance(activities, list):
            activities = [activities]

        for activity in activities:
            self.activities.append(activity)

    def retrieve_activity(self):
        return self.activities

    def pay_with_card(self, target: "User", amount: float, note: str) -> Payment:
        amount = float(amount)

        if self.username == target.username:
            raise PaymentException("User cannot pay themselves.")

        elif amount <= 0.0:
            raise PaymentException("Amount must be a non-negative number.")

        elif self.credit_card_number is None:
            raise PaymentException("Must have a credit card to make a payment.")

        self._charge_credit_card(self.credit_card_number)
        payment = Payment(amount, self, target, note)
        target.add_to_balance(amount)

        return payment

    def pay_with_balance(self, target: "User", amount: float, note: str):
        # TODO: add code here

        if self.username == target.username:
            raise PaymentException("User cannot pay themselves.")

        if self.balance < amount or self.balance == 0:
            raise BalanceException("No available amount for paying with balance")

        self.remove_from_balance(amount=amount)
        target.add_to_balance(amount=amount)
        payment = Payment(amount, self, target, note)

        return payment

    def _is_valid_credit_card(self, credit_card_number):
        return credit_card_number in ["4111111111111111", "4242424242424242"]

    def _is_valid_username(self, username):
        return re.match("^[A-Za-z0-9_\\-]{4,15}$", username)

    def _charge_credit_card(self, credit_card_number):
        # magic method that charges a credit card thru the card processor
        pass

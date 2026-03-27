import re
import unittest
import uuid


class UsernameException(Exception):
    pass


class PaymentException(Exception):
    pass


class CreditCardException(Exception):
    pass


class Payment:

    def __init__(self, amount, actor, target, note):
        self.id = str(uuid.uuid4())
        self.amount = float(amount)
        self.actor = actor
        self.target = target
        self.note = note


class User:

    def __init__(self, username):
        self.credit_card_number = None
        self.balance = 0.0

        if self._is_valid_username(username):
            self.username = username
        else:
            raise UsernameException("Username not valid.")

    def retrieve_feed(self):
        # TODO: add code here
        return []

    def add_friend(self, new_friend):
        # TODO: add code here
        pass

    def add_to_balance(self, amount):
        self.balance += float(amount)

    def add_credit_card(self, credit_card_number):
        if self.credit_card_number is not None:
            raise CreditCardException("Only one credit card per user!")

        if self._is_valid_credit_card(credit_card_number):
            self.credit_card_number = credit_card_number

        else:
            raise CreditCardException("Invalid credit card number.")

    def pay(self, target, amount, note):
        # TODO: add logic to pay with card or balance
        pass

    def pay_with_card(self, target, amount, note):
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

    def pay_with_balance(self, target, amount, note):
        # TODO: add code here
        pass

    def _is_valid_credit_card(self, credit_card_number):
        return credit_card_number in ["4111111111111111", "4242424242424242"]

    def _is_valid_username(self, username):
        return re.match("^[A-Za-z0-9_\\-]{4,15}$", username)

    def _charge_credit_card(self, credit_card_number):
        # magic method that charges a credit card thru the card processor
        pass


class MiniVenmo:
    def create_user(self, username: str, balance: float, credit_card_number: str):
        # TODO: add code here
        return User(username=username)

    def render_feed(self, feed):
        # Bobby paid Carol $5.00 for Coffee
        # Carol paid Bobby $15.00 for Lunch
        # TODO: add code here
        pass

    @classmethod
    def run(cls):
        venmo = cls()

        bobby = venmo.create_user("Bobby", 5.00, "4111111111111111")
        carol = venmo.create_user("Carol", 10.00, "4242424242424242")

        try:
            # should complete using balance
            bobby.pay(carol, 5.00, "Coffee")

            # should complete using card
            carol.pay(bobby, 15.00, "Lunch")
        except PaymentException as e:
            print(e)

        feed = bobby.retrieve_feed()
        venmo.render_feed(feed)

        bobby.add_friend(carol)


class TestUser(unittest.TestCase):

    def test_this_works(self):
        with self.assertRaises(UsernameException):
            raise UsernameException()

    def test_run(self):
        MiniVenmo.run()

    def test_user_card_payment(self):
        venmo = MiniVenmo()

        bobby = venmo.create_user("Bobby", 5.00, "4111111111111111")
        carol = venmo.create_user("Carol", 10.00, "4242424242424242")

        try:
            # should complete using balance
            bobby.pay(carol, 5.00, "Coffee")

            self.assertEqual(bobby.balance, 0)
            self.assertEqual(carol.balance, 15)

            # should complete using card
            carol.pay(bobby, 15.00, "Lunch")
        except PaymentException as e:
            print(e)

        feed_bobby = bobby.retrieve_activity()
        feed_carol = carol.retrieve_activity()

        self.assertEqual(len(feed_bobby), 1)
        self.assertEqual(len(feed_carol), 1)

    def test_user_friend(self):
        venmo = MiniVenmo()

        bobby = venmo.create_user("Bobby", 5.00, "4111111111111111")
        carol = venmo.create_user("Carol", 10.00, "4242424242424242")

        bobby.add_friend(carol)

        self.assertEqual(len(bobby.friends), 1)

    def test_insufficient_balance(self):
        venmo = MiniVenmo()

        bobby = venmo.create_user("Bobby", 1.00, "4111111111111111")
        carol = venmo.create_user("Carol", 10.00, "4242424242424242")

        try:
            bobby.pay(carol, 5.00, "Coffee")
        except PaymentException as e:
            print(e)

        # checks for credits card charges
        self.assertEqual(bobby.balance, 1)
        self.assertEqual(len(bobby.activities), 1)
        self.assertEqual(bobby.activities[0].amount, 5)


if __name__ == "__main__":
    unittest.main()

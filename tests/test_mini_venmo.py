import unittest

from controllers import MiniVenmo
from exceptions import PaymentException, UsernameException


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

from typing import NoReturn

from entities import Payment, User, UserAddEvent


class MiniVenmo:
    def create_user(
        self, username: str, balance: float, credit_card_number: str
    ) -> User:
        user = User(username)
        user.add_credit_card(credit_card_number)
        user.add_to_balance(balance)

        user.useradd_event_callback = self.render_feed

        return user

    def render_feed(self, feed) -> NoReturn:
        # Bobby paid Carol $5.00 for Coffee
        # Carol paid Bobby $15.00 for Lunch
        for activity in feed:
            if isinstance(activity, UserAddEvent):
                print(
                    f"{activity.actor.username} added {activity.target.username} as Friend"
                )
            elif isinstance(activity, Payment):
                print(
                    f"{activity.actor.username} paid {activity.target.username} ${activity.amount} for {activity.note} "
                )

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

        feed = bobby.retrieve_activity()
        venmo.render_feed(feed)

        bobby.add_friend(carol)

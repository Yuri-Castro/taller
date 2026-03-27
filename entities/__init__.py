import uuid


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

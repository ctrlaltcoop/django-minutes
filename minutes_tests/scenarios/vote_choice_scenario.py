from django.contrib.auth.models import User
from minutes.auth.models import Token, TokenTypes

from minutes.models import VoteChoice


class VoteChoiceScenario:
    def __init__(self):
        self.admin = User.objects.create(is_staff=True, username='admin')
        self.admin_token = Token.objects.create(user=self.admin, token_type=TokenTypes.AUTH)

        self.user = User.objects.create(username='user')
        self.user_token = Token.objects.create(user=self.user, token_type=TokenTypes.AUTH)

        self.vote_choice_1 = VoteChoice.objects.create(name="Test Choice 1")
        self.vote_choice_2 = VoteChoice.objects.create(name="Test Choice 2")
        self.vote_choice_3 = VoteChoice.objects.create(name="Test Choice 3")

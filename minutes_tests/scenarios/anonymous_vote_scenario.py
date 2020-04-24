from minutes.models import Decision, AnonymousVote, VoteChoice
from minutes_tests.scenarios.agendaitem_scenario import AgendaItemScenario
from minutes_tests.scenarios.decision_scenario import DecisionScenario


class AnonymousVoteScenario(DecisionScenario):
    def __init__(self):
        super().__init__()
        self.dummy_vote_class = VoteChoice.objects.create(name='dummy')
        self.anonymous_vote = AnonymousVote.objects.create(
            decision=self.decision, amount=1, vote_class=self.dummy_vote_class
        )
        self.another_anonymous_vote = AnonymousVote.objects.create(
            decision=self.another_decision, amount=3, vote_class=self.dummy_vote_class
        )
        self.meeting_2_vote = AnonymousVote.objects.create(
            decision=self.meeting_2_agenda_item_decision, amount=5, vote_class=self.dummy_vote_class
        )

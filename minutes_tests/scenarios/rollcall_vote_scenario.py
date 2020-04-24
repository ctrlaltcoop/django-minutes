from minutes.models import Decision, AnonymousVote, VoteChoice, RollCallVote
from minutes_tests.scenarios.agendaitem_scenario import AgendaItemScenario
from minutes_tests.scenarios.decision_scenario import DecisionScenario


class RollCallVoteScenario(DecisionScenario):
    def __init__(self):
        super().__init__()
        self.dummy_vote_class = VoteChoice.objects.create(name='dummy')
        self.rollcall_vote = RollCallVote.objects.create(
            decision=self.decision, user=self.nobody, vote_class=self.dummy_vote_class
        )
        self.another_rollcall_vote = RollCallVote.objects.create(
            decision=self.another_decision, user=self.nobody, vote_class=self.dummy_vote_class
        )
        self.meeting_2_rollcallvote = RollCallVote.objects.create(
            decision=self.meeting_2_agenda_item_decision, user=self.nobody, vote_class=self.dummy_vote_class
        )

from minutes.models import Decision
from minutes_tests.scenarios.agendaitem_scenario import AgendaItemScenario


class DecisionScenario(AgendaItemScenario):
    def __init__(self):
        super().__init__()
        self.decision = Decision.objects.create(agenda_item=self.agenda_item)
        self.another_decision = Decision.objects.create(agenda_item=self.another_agenda_item)
        self.meeting_2_agenda_item_decision = Decision.objects.create(agenda_item=self.meeting_2_agenda_item)

from minutes.models import AgendaSubItem
from minutes_tests.scenarios.agendaitem_scenario import AgendaItemScenario


class AgendaSubItemScenario(AgendaItemScenario):
    def __init__(self):
        super().__init__()
        self.subitem = AgendaSubItem.objects.create(agenda_item=self.agenda_item)
        self.another_subitem = AgendaSubItem.objects.create(agenda_item=self.another_agenda_item)
        self.meeting_2_agenda_item_subitem = AgendaSubItem.objects.create(agenda_item=self.meeting_2_agenda_item)

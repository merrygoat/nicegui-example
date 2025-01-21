from typing import TYPE_CHECKING, Iterable

import nicegui.events
from nicegui import ui

from nicegui_template.models import Party, Candidate

if TYPE_CHECKING:
    from nicegui_template.main import UIMainForm


class UIParties:
    def __init__(self, parent: "UIMainForm"):
        self.parent = parent

        ui.html("Party membership").classes("text-2xl")
        self.party_select = ui.select(label="Party", options=[], on_change=self.update_members_grid).classes("min-w-[400px]").props('popup-content-class="!max-h-[500px]"')

        self.party_members_grid = ui.aggrid({
            'defaultColDef': {"suppressMovable": True},
            'columnDefs': [{"headerName": "id", "field": "id", "hide": True},
                           {"headerName": "First Name", "field": "first_name", "sort": "asc", "sortIndex": 1},
                           {"headerName": "Last Name", "field": "last_name", "sort": "asc", "sortIndex": 0},
                           {"headerName": "Email", "field": "email"}],
            'rowData': {},
        })

        self.populate_party_select()

    def populate_party_select(self):
        parties = Party.select()
        parties = {party.id: party.name for party in parties}
        self.party_select.set_options(parties)

    def update_members_grid(self, event: nicegui.events.ValueChangeEventArguments):
        selected_party_id = event.sender.value

        candidates: Iterable[Candidate] = Candidate.select().where(Candidate.party == selected_party_id)

        candidate_details = []
        for candidate in candidates:
            details = {"id": candidate.id, "first_name": candidate.first_name, "last_name": candidate.last_name, "email": candidate.email}

            candidate_details.append(details)

        self.party_members_grid.options["rowData"] = candidate_details
        self.party_members_grid.update()

from typing import TYPE_CHECKING, Iterable

from nicegui import ui

from nicegui_template.models import Party, Candidate

if TYPE_CHECKING:
    from nicegui_template.main import UIMainForm


class UICandidates:
    def __init__(self, parent: "UIMainForm"):
        self.parent = parent

        ui.html("Candidates").classes("text-2xl")
        self.account_grid = ui.aggrid({
            'defaultColDef': {"suppressMovable": True},
            'columnDefs': [{"headerName": "id", "field": "id", "hidden": "true"},
                           {"headerName": "First Name", "field": "first_name", "sort": "asc", "sortIndex": 1},
                           {"headerName": "Last Name", "field": "last_name", "sort": "asc", "sortIndex": 0},
                           {"headerName": "Party", "field": "party"}],
            'rowData': {},
        })

        self.populate_candidates()

    def populate_candidates(self):
        candidates: Iterable[Candidate] = (Candidate.select()
                                           .join(Party))
        candidate_details = []
        for candidate in candidates:
            candidate_details.append({"first_name": candidate.first_name, "last_name": candidate.last_name,
                                      "party": candidate.party.name})
        self.account_grid.options["rowData"] = candidate_details

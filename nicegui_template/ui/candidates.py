from typing import TYPE_CHECKING, Iterable

from nicegui import ui
from peewee import JOIN

from nicegui_template.models import Party, Candidate

if TYPE_CHECKING:
    from nicegui_template.main import UIMainForm


class UICandidates:
    def __init__(self, parent: "UIMainForm"):
        self.parent = parent

        self.new_candidate_dialog = UIDialogNewCandidate(self)

        ui.html("Candidates").classes("text-2xl")
        self.candidate_grid = ui.aggrid({
            'defaultColDef': {"suppressMovable": True},
            'columnDefs': [{"headerName": "id", "field": "id", "hide": True},
                           {"headerName": "First Name", "field": "first_name", "sort": "asc", "sortIndex": 1},
                           {"headerName": "Last Name", "field": "last_name", "sort": "asc", "sortIndex": 0},
                           {"headerName": "Email", "field": "email"},
                           {"headerName": "Party", "field": "party"}],
            'rowSelection': 'single',
            'rowData': {},
        })
        with ui.row():
            self.new_candidate_button = ui.button("Add new candidate", on_click=self.new_candidate_dialog.open)
            self.delete_candidate_button = ui.button("Delete selected candiate", on_click=self.delete_selected_candidate)

        self.populate_candidate_grid()

    def populate_candidate_grid(self):
        candidates: Iterable[Candidate] = (Candidate.select().join(Party, JOIN.LEFT_OUTER))
        candidate_details = []
        for candidate in candidates:
            details = {"id": candidate.id, "first_name": candidate.first_name, "last_name": candidate.last_name, "email": candidate.email}
            if candidate.party:
                details["party"] = candidate.party.name
            else:
                details["party"] = None
            candidate_details.append(details)

        self.candidate_grid.options["rowData"] = candidate_details
        self.candidate_grid.update()

    async def delete_selected_candidate(self):
        row = await(self.candidate_grid.get_selected_row())
        if row:
            candidate_id = row["id"]
            Candidate.delete().where(Candidate.id == candidate_id).execute()
            ui.notify("Candidate deleted")
            self.populate_candidate_grid()
        else:
            ui.notify("No candidate selected to edit.")


class UIDialogNewCandidate:
    def __init__(self, parent: "UICandidates"):
        self.parent = parent

        with ui.dialog() as self.dialog:
            with ui.card():
                ui.label("New candidate").classes("text-2xl")
                with ui.grid(columns="auto auto"):
                    ui.label("First Name")
                    self.first_name_input = ui.input(validation={"Must provide first name": lambda value: len(value) > 0})
                    ui.label("Last Name")
                    self.last_name_input = ui.input(validation={"Must provide last name": lambda value: len(value) > 0})
                    ui.label("Email")
                    self.email_input = ui.input(validation={"Must provide email": lambda value: len(value) > 0})
                    ui.label("Party")
                    self.party_select = ui.select(options=[])
                    ui.button("Add", on_click=self.add_new_candidate)
                    ui.button("Cancel", on_click=self.dialog.close)
        self.populate_party_select()

    def open(self):
        self.dialog.open()

    def close(self):
        self.dialog.close()

    def populate_party_select(self):
        parties = Party.select()
        parties = {party.id: party.name for party in parties}
        self.party_select.set_options(parties)

    def add_new_candidate(self):
        first_name = self.first_name_input.value
        last_name = self.last_name_input.value
        email = self.email_input.value

        if not first_name:
            ui.notify("Must specify first name")
            return 0
        if not last_name:
            ui.notify("Must specify last name")
            return 0
        if not email:
            ui.notify("Must specify email")
            return 0

        # This field is optional so may return none, this is not a problem as peewee will happily set a None value for
        # an optional field.
        party = self.party_select.value

        Candidate.create(first_name=first_name, last_name=last_name, email=email, party=party)
        ui.notify("New candidate created.")
        self.parent.populate_candidate_grid()
        self.close()
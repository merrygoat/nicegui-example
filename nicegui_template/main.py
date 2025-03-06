from nicegui import ui, app

from nicegui_template import initialization

import logging

from nicegui_template.ui.candidates import UICandidates
from nicegui_template.ui.parties import UIParties

# This logging allows viewing of raw SQL queries in the console as they are made by peewee
logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

def main():
    app.on_startup(initialization.initialize)
    app.on_exception(lambda e: ui.notify(f"Exception: {e}"))
    ui.run()


@ui.page('/')
def home():
    UIMainForm()


class UIMainForm:
    def __init__(self):

        with ui.splitter(value=150).props("unit=px").classes('w-full h-full') as splitter:
            with splitter.before:
                with ui.tabs().props('vertical').classes('w-full') as tabs:
                    self.accounts_tab = ui.tab('Candidates', icon='person')
                    self.transactions_tab = ui.tab('Parties', icon='flag')
            with splitter.after:
                with ui.tab_panels(tabs, value=self.accounts_tab).props('vertical').classes('w-full h-full'):
                    with ui.tab_panel(self.accounts_tab):
                        self.account_details = UICandidates(self)
                    with ui.tab_panel(self.transactions_tab):
                        self.parties = UIParties(self)


main()

from nicegui import ui

from nicegui_template.models import Candidate, Party


def initialize():
    add_sample_data()
    # You can set default properties/classes which are then used by all subsequently declared ui objects of that type
    ui.input.default_props("dense outlined")
    ui.textarea.default_props("outlined")
    ui.select.default_props("outlined")
    ui.label.default_classes("place-content-center")

def add_sample_data():
    people = [candidate for candidate in Candidate.select()]
    parties = [party for party in Party.select()]
    if not people and not parties:
        sensible = Party.create(name="Sensible Party")
        silly = Party.create(name="Silly Party")
        Candidate.create(first_name="Arthur", last_name="Smith", email="bob@internet.com", party=sensible)
        Candidate.create(first_name="Jethro", last_name="Walrustitty", email="eric@internet.com", party=silly)

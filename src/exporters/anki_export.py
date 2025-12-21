from typing import List

import genanki
from core.cards import Flashcard

MODEL_BASIC = genanki.Model(
    1607392319,
    "Basic FR",
    fields=[{"name": "Front"}, {"name": "Back"}],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Front}}",
            "afmt": '{{Front}}<hr id="answer">{{Back}}',
        }
    ],
)

MODEL_BASIC_REV = genanki.Model(
    998877661,
    "Basic (and reversed) FR",
    fields=[{"name": "Front"}, {"name": "Back"}],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Front}}",
            "afmt": '{{Front}}<hr id="answer">{{Back}}',
        },
        {
            "name": "Card 2",
            "qfmt": "{{Back}}",
            "afmt": '{{Back}}<hr id="answer">{{Front}}',
        },
    ],
)

NOTE_TYPE_MAP = {
    "Basic": MODEL_BASIC,
    "Basic (and reversed)": MODEL_BASIC_REV,
}


def export_apkg(cards: List[Flashcard], deck_name: str, out_path: str):
    deck = genanki.Deck(2059400110, deck_name)
    for c in cards:
        model = NOTE_TYPE_MAP.get(c.note_type, MODEL_BASIC)
        note = genanki.Note(
            model=model, fields=[c.front, c.back], guid=c.guid, tags=c.tags
        )
        deck.add_note(note)
    pkg = genanki.Package(deck)
    pkg.write_to_file(out_path)

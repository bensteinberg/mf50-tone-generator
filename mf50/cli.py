import click
import pickle
import requests
import camelot
import pandas as pd
from pathlib import Path


@click.command()
@click.option(
    "--pdf",
    default="MicroFox-50_Manual_v0.2.pdf",
    help="The source of the MicroFox 50 tone codes",
)
@click.option(
    "--sequence",
    default=(" 3 3 *** 3 3 *** 6 6 /// 6 6 /// 9 9 333 9 9 333 ; ; 666 ; ; 666"),
)
@click.option(
    "--source",
    type=click.Choice(["fox", "tidal"], case_sensitive=False),
    default="fox",
    show_default=True,
)
def doit(pdf, sequence, source):
    """This program translates between the sequencing syntax of the Byonics MicroFox 50 and TidalCycles notes."""
    notes = get_notes(pdf)

    def transl(fr, to, val, d=notes):
        """Translates val in d from fr key to to key"""
        return [n[to] for n in d if n[fr] == val][0]

    def tidalize(sequence):
        return " ".join([transl("char", "tidal", char) for char in list(sequence)])

    def foxize(sequence):
        return "".join([transl("tidal", "char", note) for note in sequence.split()])

    if source == "fox":
        f = tidalize
    elif source == "tidal":
        f = foxize

    click.echo(f(sequence))


def get_notes(pdf, base_url="https://byonics.com/downloads"):
    """Cache the notes in a pickle."""
    pkl = Path(f"{pdf}.pkl")

    try:
        with open(pkl, "rb") as f:
            notes = pickle.load(f)
    except FileNotFoundError:
        notes = []

        if not Path(pdf).exists():
            r = requests.get(f"{base_url}/{pdf}")
            with open(pdf, "wb") as f:
                f.write(r.content)

        tables = camelot.read_pdf(f"{pdf}", pages="1-end")

        for a, b in [(a, a + 3) for a in range(1, 20, 5)]:
            c = pd.concat([tables[0].df.iloc[1:, a:b]] + [tables[1].df.iloc[:, a:b]])
            c.columns = ["note", "freq", "char"]
            notes.append(c.to_dict("records"))

        # remove empty(-ish) rows
        notes = [n for n in [x for y in notes for x in y] if n["freq"]]

        assert len(notes) == 48

        for n in notes:
            n.update({"tidal": n["note"].lower().replace("#", "s").replace("\n", "")})

        # add back rest
        notes.append({"note": "silence", "freq": "", "char": " ", "tidal": "~"})

        with open(pkl, "wb") as f:
            pickle.dump(notes, f)

    return notes

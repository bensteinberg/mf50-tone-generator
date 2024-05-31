mf50-tone-generator
===================

This is a tool for translating between notes used by the Byonics
MicroFox 50, those used by Tidalcycles, and frequencies. The idea is
to be able to generate and test out new sequences in Tidal before
loading them into the MicroFox.

Installation and usage
----------------------

```
git clone https://github.com/bensteinberg/mf50-tone-generator.git
cd mf50-tone-generator
poetry install
poetry run doit --help
```

or simply

```
pip install git+https://github.com/bensteinberg/mf50-tone-generator.git
doit --help
```

in a virtual environment.

You could take the Tidal version of the default sequence (obtained by
running `doit`) and play it something like this:

```
setcps (0.3125)

d1 $ n "~ ds5 ~ ds5 ~ fs4 fs4 fs4 ~ ds5 ~ ds5 ~ fs4 fs4 fs4 ~ fs5 ~ fs5 ~ b4 b4 b4 ~ fs5 ~ fs5 ~ b4 b4 b4 ~ a5 ~ a5 ~ ds5 ds5 ds5 ~ a5 ~ a5 ~ ds5 ds5 ds5 ~ b5 ~ b5 ~ fs5 fs5 fs5 ~ b5 ~ b5 ~ fs5 fs5 fs5" # s "superfm"
```

There is some clicking; I haven't yet figured out how to filter it or
use an envelope. The cycles per second value of 0.3125 is

```
1 second / (64 steps * 0.05 seconds)
```

where 0.05s aka 50ms is the default length of a note in the MF50.

Notes
-----

I settled on the convention of using `0` for the frequency of a
rest. It could be something else; if you were to change it in
`get_notes()`, you'd have to delete the pickle file to get it to be
true.

from music21 import *

def test_midi():
    a = converter.parse('tests/sample.musicxml').write('midi')
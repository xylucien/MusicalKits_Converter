from music21 import *

def test_midi():
    result = converter.parse('tests/sample.musicxml').write('midi')
def test_midi_long():
    result = converter.parse('tests/ActorPreludeSample.musicxml').write('midi')
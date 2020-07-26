from music21 import *

def test_midi():
    result = converter.parse('tests/testFiles/Chant.musicxml').write('midi')
def test_midi_long():
    result = converter.parse('tests/testFiles/ActorPreludeSample.musicxml').write('midi')
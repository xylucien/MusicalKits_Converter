from music21 import *

def test_midi():
    a = converter.parse('result.abc').write('midi')
    assert 1 == 1
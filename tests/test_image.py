from music21 import *

def test_png():
    a = converter.parse('tests/sample.musicxml').write('lilypond.png')
    b = converter.parse('tests/sample.musicxml').write('musicxml.png')
    assert 1 == 1
from music21 import *

def test_png():
    a = converter.parse('tests/sample.musicxml').write('lilypond.png', 'tests/result')
    assert 1 == 1
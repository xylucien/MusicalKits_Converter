from music21 import *

def test_png_lilypond():
    a = converter.parse('tests/sample.musicxml').write('lilypond.png')
def test_png_mscore():   
    b = converter.parse('tests/ActorPreludeSample.musicxml').write('musicxml.png')
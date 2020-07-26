from music21 import *

def test_png_lilypond():
    a = converter.parse('tests/sample.musicxml').write('lilypond.png')
def test_png_mscore_from_mxl_short():   
    easy_task = converter.parse('tests/sample.musicxml').write('musicxml.png')
def test_png_mscore_from_mxl_long(): 
    long_task = converter.parse('tests/ActorPreludeSample.musicxml').write('musicxml.png')
def test_png_mscore_from_midi():
    long_midi_task = converter.parse('tests/Super_Mario_64.mid').write('musicxml.png')
    
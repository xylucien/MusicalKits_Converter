from converter.convert import Convert
import io

def test_submit_InvalidMusicXml(test_client):
    #Test can upload and detect invalid musicxml.
    data = {"text": "abcde", "format": ".musicxml"}
    data = {key: str(value) for key, value in data.items()}
    response = test_client.post(
        '/convert_result/submission', data=data, follow_redirects=True
    )
    assert b'"is_success": false' in response.data

def test_submit_InvalidABC(test_client):
    #Test can upload and detect invalid ABC.
    data = {"text": "abcde", "format": ".abc"}
    data = {key: str(value) for key, value in data.items()}
    response = test_client.post(
        '/convert_result/submission', data=data, follow_redirects=True
    )
    assert b'"is_success": false' in response.data

def test_submit_MusicXml_long(test_client):
    #Test can upload and convert long valid musicxml text.
    with open('tests/testFiles/ActorPreludeSample.musicxml', 'r') as myfile:
        filedata = myfile.read()
    data = {"text": filedata, "format": ".musicxml"}
    data = {key: str(value) for key, value in data.items()}
    
    response = test_client.post(
        '/convert_result/submission', data=data, follow_redirects=True
    )
    assert b'"is_success": true' in response.data

def test_submit_ABC_long(test_client):
    #Test can upload and convert long valid ABC text.
    with open('tests/testFiles/ActorPreludeSample.abc', 'r') as myfile:
        filedata = myfile.read()
    data = {"text": filedata, "format": ".abc"}
    data = {key: str(value) for key, value in data.items()}
    
    response = test_client.post(
        '/convert_result/submission', data=data, follow_redirects=True
    )
    assert b'"is_success": true' in response.data
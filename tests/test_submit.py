from converter.convert import Convert
import io

def test_submit_IncorrectMusicXml(test_client):
    #Test can upload and detect incorrect text.
    data = {"text": "abcde", "format": ".musicxml"}
    data = {key: str(value) for key, value in data.items()}
    response = test_client.post(
        '/convert_result/submission', data=data, follow_redirects=True
    )
    assert b'"is_success": false' in response.data

def test_submit_CorrectMusicXml(test_client):
    #Test can upload and convert valid text.
    with open('tests/sample.musicxml', 'r') as myfile:
        filedata = myfile.read()
    data = {"text": filedata, "format": ".musicxml"}
    data = {key: str(value) for key, value in data.items()}
    
    response = test_client.post(
        '/convert_result/submission', data=data, follow_redirects=True
    )
    assert b'"is_success": true' in response.data
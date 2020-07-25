from converter.convert import Convert
import io

def test_upload_IncorrectMusicXml(test_client):
    #Test can upload incorrect MusicXML
    data = {}
    data = {key: str(value) for key, value in data.items()}
    data['file'] = (io.BytesIO(b"abcdef"), 'test.musicxml')
    response = test_client.post(
        '/convert_result/upload', data=data, follow_redirects=True,
        content_type='multipart/form-data'
    )
    #assert b"Upload File" in response.data

def test_upload_CorrectMusicXml(test_client):
    #Test can upload and convert valid musicxml
    data = {}
    data = {key: str(value) for key, value in data.items()}
    data['file'] = open("tests/sample.musicxml", "rb")
    response = test_client.post(
        '/convert_result/upload', data=data, follow_redirects=True,
        content_type='multipart/form-data'
    )
    #assert b"Result" in response.data
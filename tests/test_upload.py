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
    assert b'"is_success": false' in response.data

def test_upload_CorrectMusicXml(test_client):
    #Test can upload and convert valid musicxml
    data = {}
    data = {key: str(value) for key, value in data.items()}
    data['file'] = open("tests/sample.musicxml", "rb")
    response = test_client.post(
        '/convert_result/upload', data=data, follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert b'"is_success": true' in response.data

def test_upload_NonvalidFormat(test_client):
    #Test can detect invalid musicxml
    data = {}
    data = {key: str(value) for key, value in data.items()}
    data['file'] = open("tests/sample.x", "rb")
    response = test_client.post(
        '/convert_result/upload', data=data, follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert b'File extension name not valid!' in response.data
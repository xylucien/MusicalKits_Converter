from converter.convert import Convert
import io

def test_upload_MusicXml1(test_client):
    #Test can upload and convert valid musicxml
    data = {}
    data = {key: str(value) for key, value in data.items()}
    data['file'] = open("tests/testFiles/ActorPreludeSample.musicxml", "rb")
    response = test_client.post(
        '/convert_result/upload', data=data, follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert b'"is_success": true' in response.data

def test_upload_MusicXml2(test_client):
    #Test can upload and convert valid musicxml
    data = {}
    data = {key: str(value) for key, value in data.items()}
    data['file'] = open("tests/testFiles/Chant.musicxml", "rb")
    response = test_client.post(
        '/convert_result/upload', data=data, follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert b'"is_success": true' in response.data

def test_upload_MusicXml3(test_client):
    #Test can upload and convert valid musicxml
    data = {}
    data = {key: str(value) for key, value in data.items()}
    data['file'] = open("tests/testFiles/Echigo-Jishi.musicxml", "rb")
    response = test_client.post(
        '/convert_result/upload', data=data, follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert b'"is_success": true' in response.data

def test_upload_MusicXml4(test_client):
    #Test can upload and convert valid musicxml
    data = {}
    data = {key: str(value) for key, value in data.items()}
    data['file'] = open("tests/testFiles/Saltarello.musicxml", "rb")
    response = test_client.post(
        '/convert_result/upload', data=data, follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert b'"is_success": true' in response.data

def test_upload_InvalidMusicXml(test_client):
    #Test can upload incorrect MusicXML
    data = {}
    data = {key: str(value) for key, value in data.items()}
    data['file'] = open("tests/testFiles/invalid.musicxml", "rb")    
    response = test_client.post(
        '/convert_result/upload', data=data, follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert b'"is_success": false' in response.data

def test_upload_MXL1(test_client):
    #Test can upload and convert valid mxl
    data = {}
    data = {key: str(value) for key, value in data.items()}
    data['file'] = open("tests/testFiles/ActorPreludeSample.mxl", "rb")
    response = test_client.post(
        '/convert_result/upload', data=data, follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert b'"is_success": true' in response.data

def test_upload_MXL2(test_client):
    #Test can upload and convert valid mxl
    data = {}
    data = {key: str(value) for key, value in data.items()}
    data['file'] = open("tests/testFiles/Chant.mxl", "rb")
    response = test_client.post(
        '/convert_result/upload', data=data, follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert b'"is_success": true' in response.data

def test_upload_MXL3(test_client):
    #Test can upload and convert valid mxl
    data = {}
    data = {key: str(value) for key, value in data.items()}
    data['file'] = open("tests/testFiles/Echigo-Jishi.mxl", "rb")
    response = test_client.post(
        '/convert_result/upload', data=data, follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert b'"is_success": true' in response.data

def test_upload_MXL4(test_client):
    #Test can upload and convert valid mxl
    data = {}
    data = {key: str(value) for key, value in data.items()}
    data['file'] = open("tests/testFiles/Saltarello.mxl", "rb")
    response = test_client.post(
        '/convert_result/upload', data=data, follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert b'"is_success": true' in response.data

def test_upload_InvalidMXL(test_client):
    #Test can detect incorrect MXL
    data = {}
    data = {key: str(value) for key, value in data.items()}
    data['file'] = open("tests/testFiles/invalid.mxl", "rb")    
    response = test_client.post(
        '/convert_result/upload', data=data, follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert b'"is_success": false' in response.data

def test_upload_ABC1(test_client):
    #Test can upload and convert valid ABC
    data = {}
    data = {key: str(value) for key, value in data.items()}
    data['file'] = open("tests/testFiles/ActorPreludeSample.abc", "rb")
    response = test_client.post(
        '/convert_result/upload', data=data, follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert b'"is_success": true' in response.data

def test_upload_ABC2(test_client):
    #Test can upload and convert valid ABC
    data = {}
    data = {key: str(value) for key, value in data.items()}
    data['file'] = open("tests/testFiles/KeysAndModes.abc", "rb")
    response = test_client.post(
        '/convert_result/upload', data=data, follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert b'"is_success": true' in response.data

def test_upload_ABC3(test_client):
    #Test can upload and convert valid ABC
    data = {}
    data = {key: str(value) for key, value in data.items()}
    data['file'] = open("tests/testFiles/Notes.abc", "rb")
    response = test_client.post(
        '/convert_result/upload', data=data, follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert b'"is_success": true' in response.data

def test_upload_InvalidABC(test_client):
    #Test can detect incorrect ABC
    data = {}
    data = {key: str(value) for key, value in data.items()}
    data['file'] = open("tests/testFiles/invalid.abc", "rb")    
    response = test_client.post(
        '/convert_result/upload', data=data, follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert b'"is_success": false' in response.data

def test_upload_Midi1(test_client):
    #Test can upload and convert valid midi
    data = {}
    data = {key: str(value) for key, value in data.items()}
    data['file'] = open("tests/testFiles/Super_Mario_64.mid", "rb")
    response = test_client.post(
        '/convert_result/upload', data=data, follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert b'"is_success": true' in response.data


def test_upload_Midi2(test_client):
    #Test can upload and convert valid midi
    data = {}
    data = {key: str(value) for key, value in data.items()}
    data['file'] = open("tests/testFiles/Wii_Channels.mid", "rb")
    response = test_client.post(
        '/convert_result/upload', data=data, follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert b'"is_success": true' in response.data

def test_upload_InvalidMidi(test_client):
    #Test can detect invalid midi
    data = {}
    data = {key: str(value) for key, value in data.items()}
    data['file'] = open("tests/testFiles/invalid.mid", "rb")
    response = test_client.post(
        '/convert_result/upload', data=data, follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert b'"is_success": false' in response.data

def test_upload_InvalidFormat(test_client):
    #Test can detect invalid musicxml
    data = {}
    data = {key: str(value) for key, value in data.items()}
    data['file'] = open("tests/testFiles/invalid_format.x", "rb")
    response = test_client.post(
        '/convert_result/upload', data=data, follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert b'File extension name not valid!' in response.data
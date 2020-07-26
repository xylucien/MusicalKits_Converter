import io, zipfile
from flask import current_app

def test_init(test_client):
    # update upload_data.musicxml
    # use the long text for testing
    data = {}
    data = {key: str(value) for key, value in data.items()}
    data['file'] = open("tests/testFiles/ActorPreludeSample.musicxml", "rb")
    response = test_client.post(
        '/convert_result/upload', data=data, follow_redirects=True,
        content_type='multipart/form-data'
    )
    assert b'"is_success": true' in response.data

def test_Download_ABC(test_client):
    response = test_client.post(
        '/get-file/abc', follow_redirects=True
    )
    assert response.status_code == 200
    #ABC format check
    assert b'X:' in response.data and b'T:' in response.data

def test_Download_MusicXML(test_client):
    response = test_client.post(
        '/get-file/musicxml', follow_redirects=True
    )
    assert response.status_code == 200
    #XML format check
    assert b'<?xml version="1.0" encoding="utf-8"?>' in response.data

def test_Download_Vexflow(test_client):
    response = test_client.post(
        '/get-file/vexflow', follow_redirects=True
    )
    assert response.status_code == 200
    #HTML format check
    assert b'!DOCTYPE html' in response.data

def test_Download_MIDI(test_client):
    response = test_client.post(
        '/get-sound', follow_redirects=True
    )
    assert response.status_code == 200
    #MIDI format header check
    assert b'MThd' in response.data

def test_Download_PNG(test_client):
    response = test_client.post(
        '/get-image', follow_redirects=True
    )
    assert response.status_code == 200
    #zip format header check
    assert b'PK' in response.data

def test_zip_file_integrity(test_client):
    test_zip = zipfile.ZipFile(current_app.config['OUTPUT_ZIP'])
    #zip file numbers check
    assert len(test_zip.namelist()) == 18    
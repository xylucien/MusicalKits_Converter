import io

def test_Download(test_client):
    pass
    '''
    with open("result.abc", "rb") as abc:
        abcStringIO = io.BytesIO(abc.read())

    response = test_client.get('/return-files',
                             follow_redirects=True)
    abcStringIO.seek(0)
    assert abcStringIO.read() in response.data 
    '''
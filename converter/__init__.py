import errno, os
from converter import convert, download, generate_image
from flask import Flask
from flask_bootstrap import Bootstrap
from music21 import *
from subprocess import PIPE, Popen
import stat

def setupAppAndCacheDirectories(app):
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    try:
        os.makedirs('musicxmlCache')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="lucien",
        UPLOAD_FOLDER = os.path.join(os.getcwd(),'musicxmlCache'),
        OUTPUT_FILE = os.path.join(os.getcwd(),'result.abc'),
        OUTPUT_IMG = os.path.join(os.getcwd(),'result.png'),
        ALLOWED_EXTENSIONS = {'musicxml'}
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    setupAppAndCacheDirectories(app)
    # apply the blueprints to the app

    app.register_blueprint(convert.bp)
    app.register_blueprint(download.bp)
    app.register_blueprint(generate_image.bp)

    app.add_url_rule("/", endpoint="index")
    
    bootstrap = Bootstrap(app)
    f = open("/home/wsgi/.music21rc", "w")
    f.write('''
    <settings encoding="utf-8">
    <preference name="autoDownload" value="deny" />
    <preference name="braillePath" />
    <preference name="debug" value="0" />
    <preference name="directoryScratch" />
    <preference name="graphicsPath" value="/usr/bin/eog" />
    <preference name="ipythonShowFormat" value="ipython.musicxml.png" />
    <preference name="lilypondBackend" value="ps" />
    <preference name="lilypondFormat" value="pdf" />
    <preference name="lilypondPath" value="/usr/bin/lilypond" />
    <preference name="lilypondVersion" />
    <localCorporaSettings />
    <localCorpusSettings />
    <preference name="manualCoreCorpusPath" />
    <preference name="midiPath" />
    <preference name="musescoreDirectPNGPath" />
    <preference name="musicxmlPath" value="/usr/bin/musescore" />
    <preference name="pdfPath" />
    <preference name="showFormat" value="musicxml" />
    <preference name="vectorPath" />
    <preference name="warnings" value="1" />
    <preference name="writeFormat" value="musicxml" />
    </settings>
    ''')
    f.close()
    process = Popen(['which' ,'lilypond'], 
        stdout=PIPE, stderr = PIPE)
    stdout, stderr = process.communicate()
    environment.set('lilypondPath', stdout.decode().replace('\n', ''))
    return app
import errno, os

from flask import Flask
from flask_bootstrap import Bootstrap

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="lucien",
        UPLOAD_FOLDER = os.path.join(os.getcwd(),'musicxmlCache'),
        OUTPUT_FILE = 'result.abc',
        ALLOWED_EXTENSIONS = {'musicxml'}
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    try:
        os.makedirs('musicxmlCache')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # apply the blueprints to the app
    from converter import convert, download

    app.register_blueprint(convert.bp)
    app.register_blueprint(download.bp)

    app.add_url_rule("/", endpoint="index")
    
    bootstrap = Bootstrap(app)

    return app
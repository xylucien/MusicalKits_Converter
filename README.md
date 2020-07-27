# MusicalKits_Converter

This project aims to provide a web service to convert between different music sheet formats. It also supports generating visaulized score and sound file. The app is hosted on Amazon Web Service Elastic Beanstalk.

Converter Script Credit: https://wim.vree.org/svgParse/xml2abc.html
Converter Core Credit: Music21, Musescore3

# Install

For local testing, do the following:

```
# Clone the repository
$ git clone https://github.com/lucien386/MusicalKits_Converter.git
$ cd MusicalKits_Converter
$ cd scripts
# run the setup script and install python package
$ sh setup.sh
$ pip3 install -e .
```
# Run
```
Linux:

$ export FLASK_APP=converter
$ flask run

Windows:

> set FLASK_APP=converter
> flask run
```
Open http://127.0.0.1:5000 in a browser.

# Test
```
$ pip3 install pytest
$ python3 -m pytest
```

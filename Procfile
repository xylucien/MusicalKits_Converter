web: gunicorn
packages: 
  yum:
    Xvfb: [] 
commands:
  lilypond_download:
    command: wget https://lilypond.org/download/binaries/linux-64/lilypond-2.20.0-1.linux-64.sh
  lilypond_install:
    command: sudo sh lilypond-2.20.0-1.linux-64.sh
  musescore_download:
    command: wget https://cdn.jsdelivr.net/musescore/v3.4.2/MuseScore-3.4.2-x86_64.AppImage
  musescore_install:
    command: sudo ./MuseScore-3.4.2-x86_64.AppImage install
  Xvfb_download:
    command: sudo yum install Xvfb
  Xvfb_configure:
    command: Xvfb :0 -screen 0 1280x768x24&
  Display_configure:
    command: export DISPLAY=:0
  Display_configure2:
    command: export DISPLAY=:0
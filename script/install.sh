pip3 install -r requirements.txt
wget https://lilypond.org/download/binaries/linux-64/lilypond-2.20.0-1.linux-64.sh
sudo sh lilypond-2.20.0-1.linux-64.sh
wget https://cdn.jsdelivr.net/musescore/v3.4.2/MuseScore-3.4.2-x86_64.AppImage
sudo ./MuseScore-3.4.2-x86_64.AppImage install
Xvfb :0 -screen 0 1280x768x24&
export DISPLAY=:0
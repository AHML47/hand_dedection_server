this is a hand detection project for raspberry pi 5 
for python development on raspberry pi you should create a python virtuel envirment and install required packages on it 
to create virtuel envirment : 
    
    python3 -m venv <name_of_venv>
to activate the venv:
    source <name_of_venv>/bin/activate

required packages : 
for camera :
    sudo apt install -y python3-libcamera python3-kms++
    sudo apt install -y python3-prctl libatlas-base-dev ffmpeg python3-pip
    sudo apt install -y python3-pyqt5 python3-opengl # only if you want GUI features
    pip3 install numpy --upgrade

    pip3 install picamera2

for robot_hat :
    sudo apt install git python3-pip python3-setuptools python3-smbus
    cd ~/
    git clone -b v2.0 https://github.com/sunfounder/robot-hat.git
    cd robot-hat
    sudo python3 setup.py install

for the webServer :
    pip install Flask

for mediapipe:
    pip install mediapipe

for open-cv :
    pip install opencv-python


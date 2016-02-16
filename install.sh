curl -O https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo -HE pip install virtualenv
# git clone https://github.com/andrewalexander/hackpsu_registration
# cd hackpsu_registration
mkdir -p ~/envs/
virtualenv ~/envs/hackpsu
source ~/envs/hackpsu/bin/activate
pip install -r requirements.txt
brew install node
sudo -HE npm install -g bower
sudo -HE npm install 
python -m SimpleHTTPServer &
python server.py &
echo "-----"
echo "Both servers are running. To quit, type 'fg', then Ctrl+C to"
echo "exit the 'python server.py' process, and then repeat for the"
echo "'python -m SimpleHTTPServer' process. When you are finished,"
echo "type 'deactivate' to exit the virtualenv"
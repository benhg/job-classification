template_string = """#!/bin/bash

sudo apt-get install -y python3
sudo apt-get install -y python3-pip
sudo pip3 install ipyparallel
sudo pip3 install parsl

cat <<EOF > ipengine.json
$ipengine_json
EOF

mkdir -p '.ipengine_logs'
ipengine --file=ipengine.json &>> .ipengine_logs/$jobname.log
"""
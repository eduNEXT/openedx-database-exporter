#! /bin/sh
# Not tested, Use at your own risk!
sudo apt-get update -y
sudo apt-get install -y build-essential software-properties-common python-software-properties curl git-core libxml2-dev libxslt1-dev libfreetype6-dev python-pip python-apt python-dev libmysqlclient-dev tree
sudo pip install --upgrade pip
sudo pip install --upgrade virtualenv

virtualenv ../venv

# Other dependencies
sudo apt-get install mysql-server  # ***REMOVED***

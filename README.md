

# Installation
```
sudo apt-get update -y
sudo apt-get install -y build-essential software-properties-common python-software-properties curl git-core libxml2-dev libxslt1-dev libfreetype6-dev python-pip python-apt python-dev libmysqlclient-dev tree
sudo pip install --upgrade pip
sudo pip install --upgrade virtualenv
sudo chmod o+w /edx/app/
virtualenv ../venv

# Other dependencies
sudo apt-get install mysql-server  # ***REMOVED***
```


# Usage
```
cd /edx/app/exports
source ../venv/bin/activate
pip install -r requirements.txt
pip install -e .
```


# databases
```
mysql -u root -p edxapp < /vagrant/data/MOAR+PATH/edxapp.sql
***REMOVED***

--extended-insert
--net_buffer_length=5000
```
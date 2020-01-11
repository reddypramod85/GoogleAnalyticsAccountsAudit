# Google-Analytics-Accounts-Audit

Utilities to audit and maintain members in the Google Analytics Accounts

Utility scripts to audit and maintain the Google Analytics Accounts members

Based on [Google Analytics Management API](https://developers.google.com/analytics/devguides/config/mgmt/v3) and [Google API Python Client](https://github.com/googleapis/google-api-python-client)


## Install instructions for Ubuntu Linux (this was done using 14.10)
Install pip
```
sudo apt-get python-pip
```

Install python virtual environments
```
sudo pip install virtualenv
```

Clone this repo
```
git checkout https://github.com/reddypramod85/Google-Analytics-Accounts-Audit.git
```

Create a virtual environment
```
cd Google-Analytics-Accounts-Audit
virtualenv venv
source venv/bin/activate
```

Install the python google api client
```
pip install google-api-python-client
```

Authorization information to Management API can be found [here](https://developers.google.com/analytics/devguides/config/mgmt/v3/authorization)

Download the secret json file of a admin user and place it in the root folder and update the config.yaml file

Install ldapsearch commmand line
```
sudo apt-get install ldap-utils
```

Setup cron job to run the GoogleAnalyticsAccountsAudit.py on a nightly basis

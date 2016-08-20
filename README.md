# pidsvcbkp

This code backs up a PID Svc server which is expected to consist of an instance of the PIDSvc with config in its database and an HTTP server in front of it which is assumed to be Apache.

This code contains only one functioning Python file (backup.py) and an example crontab file to run it daily. Any changes detected in either the PIDSvc's DB or in Apache's config will be backed up to a remote Git repo.

This code only runs on Linux and requires a remote Git repo to hold backups remotely.


### How to use

1. Clone this repo somewhere on the PIDSvc machine
2. Create a blank Git repo that you want to back this machine up to
3. Clone that backup repo to somewhere on the PIDSvc machine
    * The location of that repo is your local backup folder
    * Your PIDSvc & Apache settings will be initially copied there and then commited back to your remote backup repo
    * You will need to have passwordless access to that repo. See http://stackoverflow.com/questions/8588768/git-push-username-password-how-to-avoid 
4. Copy the settings.json file in this repo, which is an incompleted template, to somewhere outside this repo
    * This file will contain settings you may want to keep secret! 
5. Set the appropriate settings in your secret settings.json file
    * In order to indicate the locations of the PIDSvc API, Apache Conf files and so on
6. Copy the contents of crontab to your crontab
    * This runs the backup each day but only backs up with a new commit if changes are detected


### Contact

Nicholas Car, Data Architect at Geoscience Australia (nicholas.car@ga.gov.au)

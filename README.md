# pidsvcbkp

This code backs up a PID Svc server which is expected to consist of one or more instances of the PID Svc Tomcat application, corresponding database(s) and an HTTP server in front of it/them which is assumed to be Apache.

This code contains only one functioning Python file, backup.py, and an example crontab file to run it daily. backup.py, when run, detects any changes in either the PIDSvc's DB(s) or in Apache's config and will then back up those changes to a nominated Git repo.

This code only runs on Linux and requires a remote Git repo to bacup to.


### How to use

1. Clone this repo somewhere on the PID Svc machine
2. Create a blank Git repo that you want to back this machine up to
3. Clone that backup repo to somewhere on the PID Svc machine
    * That local repo is where your PID Svc DBs and Apache config files are initially backed up to 
    * The local Git repo then pushes changes to the remote repo
        * You will need to have passwordless access to that repo. See http://stackoverflow.com/questions/8588768/git-push-username-password-how-to-avoid 
4. Copy the settings.json file in this repo, which is a template needing completion, to somewhere outside this repo
    * This file will contain settings you may want to keep secret! 
5. Set the appropriate settings in your secret settings.json file
    * In order to indicate the locations of the PID Svc API, Apache Conf files and so on
6. Copy the contents of crontab to your crontab
    * This runs the backup each day but only backs up with a new local commit and remote push if changes are detected
    * Ensure you nominate the correct location for settings.py!

You can test the code and your settings by simply running:

> \# python backup.py {YOUR_SETTINGS_FILE_LOCATION}

This is the same as the command crontab will run each day.

NOTE: test runs and crontab runs must all be operated by the same user that created the Deployment Key for the Git account. Thus if you create a Deployment Key as user 'fred', you cannot run the backup.py function as root. Your local backups repo folder will need to have permissions for your key-creating user.


#### License
* Creative Commons BY 4.0, see [LICENSE](LICENSE)


## Authors and Contact
**Nicholas Car**  
Geoscience Australia  
<nicholas.car@ga.gov.au>

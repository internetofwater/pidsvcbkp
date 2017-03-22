import sys
from datetime import datetime
import json
import requests
import io
from lxml import etree
import glob
import shutil
import os
import git


class PidSvcBackupException(Exception):
    pass


# backup PID Svc Data Store via API
def backup_pidsvc(pidsvc_api_uri, backups_dir, pidsvc_bkp_file, pidsvc_usr, pidsvc_pwd):
    # see https://www.seegrid.csiro.au/wiki/Siss/PIDServiceAPI#Partial_47Full_Data_Store_Backup
    backup_url = pidsvc_api_uri + '?cmd=partial_backup' \
                               '&deprecated=false' \
                               '&lookup=true' \
                               '&format=xml'

    r = requests.get(backup_url, stream=True, auth=(pidsvc_usr, pidsvc_pwd))
    if r.status_code == 200:
        # set backup file path
        filepath = backups_dir + pidsvc_bkp_file

        # save XML file, pretty printed
	xml_tree = etree.fromstring(r.content)
        with open(filepath, 'wb') as f:
            f.write(etree.tostring(xml_tree, pretty_print=True))

        return True
    else:
        raise PidSvcBackupException('PID Svc Data Store backup failed: ' + str(r.status_code) + ', ' + r.text)


def backup_pidsvcs_all(backups_dir, pidsvcs):
    for pidsvc in pidsvcs:
        backup_pidsvc(pidsvc['api_uri'], backups_dir, pidsvc['bkp_file'], pidsvc['usr'], pidsvc['pwd'])


def backup_apache(apache_conf_file_path, backups_dir, apache_conf_bkp_file):
    shutil.copyfile(apache_conf_file_path, os.path.join(backups_dir, apache_conf_bkp_file))

    return True


def backup_apaches_all(backups_dir, apaches):
    for apache in apaches:
        backup_apache(apache['path'], backups_dir, apache['bkp_file'])


def send_backups_to_git(backups_dir):
    repo = git.Repo(backups_dir)
    # add all files
    for f in glob.glob(backups_dir):
        repo.git.add(f)
    repo.git.commit(m='backup')
    # http://stackoverflow.com/questions/8588768/git-push-username-password-how-to-avoid
    repo.git.push()

    return True


if __name__ == "__main__":
    # populated settings from a runtime nominated settings.json file
    settings = json.load(open(sys.argv[1]))

    # backup all PID Svcs data
    backup_pidsvcs_all(settings['backups_dir'], settings['pidsvcs'])

    # backup all Apache confs
    backup_apaches_all(settings['backups_dir'], settings['apaches'])

    # push backups to Git repo
    try:
        send_backups_to_git(settings['backups_dir'])
    except Exception as e:
        print(e)

from datetime import datetime
import json
import requests
import StringIO
from lxml import etree
import git


class PidSvcBackupException(Exception):
    pass


# backup PID Svc Data Store via API
def backup_pid_svc(pid_api_uri, backups_dir, pid_bkp_file):

    # see https://www.seegrid.csiro.au/wiki/Siss/PIDServiceAPI#Partial_47Full_Data_Store_Backup
    backup_url = pid_api_uri + '?cmd=partial_backup' \
                               '&deprecated=false' \
                               '&lookup=true' \
                               '&format=xml'

    r = requests.get(backup_url, stream=True)
    if r.status_code == 200:
        # write retrieved XML to a file-like object
        raw_xml = StringIO.StringIO()
        for chunk in r.iter_content(1024):
            raw_xml.write(chunk)

        # set backup file path
        filepath = backups_dir + pid_bkp_file

        # save XML file pretty printed
        xml_tree = etree.fromstring(raw_xml.getvalue())
        with open(filepath, 'w') as f:
            f.write(etree.tostring(xml_tree, pretty_print=True))

        return True
    else:
        raise PidSvcBackupException('PID Svc Data Store backup failed: ' + str(r.status_code) + ', ' + r.text)


def backup_apache_config(conf_file_paths, backups_dir, apache_bkp_file):
    # get each file, cconcatenate it into one conf file
    conf_file = backups_dir + apache_bkp_file
    with open(conf_file, 'w') as outfile:
        for f in conf_file_paths:
            outfile.write('#\n')
            outfile.write('# ' + f)
            outfile.write('#\n')
            with open(f) as infile:
                outfile.write(infile.read())

    return True


def send_backups_to_git(backups_dir):
    repo = git.Repo(backups_dir)
    repo.git.add(u=True)
    repo.git.commit(m='backup')
    # http://stackoverflow.com/questions/8588768/git-push-username-password-how-to-avoid
    repo.git.push()

    return True


if __name__ == "__main__":
    # populated settings & credentials
    settings = json.load(open('/opt/backups/settings.json'))

    # run PID SVC backup
    backup_pid_svc(settings['pid_api_uri'], settings['backups_dir'], settings['pid_bkp_file'])

    # backup Apache config
    conf_file_paths = [
        '/etc/httpd/sites-available/default.conf'
    ]
    backup_apache_config(conf_file_paths, settings['backups_dir'], settings['apache_bkp_file'])

    # push backups to Git repo
    try:
        send_backups_to_git(settings['backups_dir'])
    except git.exc.GitCommandError:
        pass

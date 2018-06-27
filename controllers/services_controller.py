# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE, call
from crontab import CronTab

class Services(object):
    """Holds information of the running services."""
    def __init__(self, app):
        super(Services, self).__init__()
        self.app = app


    def is_vnc_running(self):
        ps = Popen('systemctl status x11vnc | grep "active (running)"', shell=True, stdout=PIPE)
        output = ps.stdout.read()
        ps.stdout.close()
        ps.wait()
        return output != ""

    def enable_vnc(self):
        call(['systemctl','enable','x11vnc'])
        call(['systemctl','start','x11vnc'])
        pass

    def disable_vnc(self):
        call(['systemctl','disable','x11vnc'])
        call(['systemctl','stop','x11vnc'])
        pass


    def is_ssh_running(self):
        ps = Popen('systemctl status ssh | grep "active (running)"', shell=True, stdout=PIPE)
        output = ps.stdout.read()
        ps.stdout.close()
        ps.wait()
        return output != ""

    def enable_ssh(self):
        call(['systemctl','enable','ssh'])
        call(['systemctl','start','ssh'])

    def disable_ssh(self):
        call(['systemctl','disable','ssh'])
        call(['systemctl','stop','ssh'])


    def is_remote_configuration_running(self):
        return self.app.config['HOST'] == '0.0.0.0'

    def enable_remote_configuration(self):
        # change server config
        file = open(self.app.root_path+"/config.cfg", "w")
        file.write('HOST = "0.0.0.0"')
        file.close()
        call(['systemctl','restart','tooloop-settings-server'])

    def disable_remote_configuration(self):
        # change server config
        file = open(self.app.root_path+"/config.cfg", "w")
        file.write('HOST = "127.0.0.1"')
        file.close()
        call(['systemctl','restart','tooloop-settings-server'])


    def is_screenshot_service_running(self):
        crontab = CronTab(user='tooloop')
        for job in crontab:
            if job.command == 'env DISPLAY=:0.0 /opt/tooloop/scripts/tooloop-screenshot' and job.is_enabled():
                return True
        return False

    def enable_screenshot_service(self):
        crontab = CronTab(user='tooloop')
        for job in crontab:
            if job.command == 'env DISPLAY=:0.0 /opt/tooloop/scripts/tooloop-screenshot' and not job.is_enabled():
                job.enable()
        crontab.write()

    def disable_screenshot_service(self):
        crontab = CronTab(user='tooloop')
        for job in crontab:
            if job.command == 'env DISPLAY=:0.0 /opt/tooloop/scripts/tooloop-screenshot' and job.is_enabled():
                job.enable(False)
        crontab.write()

    def get_status(self):
        return {
            'vnc': self.is_vnc_running(),
            'ssh': self.is_ssh_running(),
            'remote_configuration': self.is_remote_configuration_running(),
            'screenshot_service': self.is_screenshot_service_running()
            }

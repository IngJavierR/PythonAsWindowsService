import win32serviceutil
import win32service
import win32event
import servicemanager
from multiprocessing import Process

import os
import sys
sys.path.append(os.path.dirname(__name__))

from main import app

class Service(win32serviceutil.ServiceFramework):
    _svc_name_ = "CinepolisService"
    _svc_display_name_ = "Cinepolis Service"
    _svc_description_ = "Cinepolis Service Scheduler"

    def __init__(self, *args):
        super().__init__(*args)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.process.terminate()
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        self.process = Process(target=self.main)
        self.process.start()
        self.process.run()

    def main(self):
        app.run(host="127.0.0.1", port=8900)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(Service)
    
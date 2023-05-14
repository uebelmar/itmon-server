import win32serviceutil
import win32service
import win32event
import servicemanager
import socket

from start import start

class MyService:
    def stop(self):
        """Stop the service"""
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            start()
            servicemanager.LogInfoMsg("Service running...")


class MyServiceFramework(win32serviceutil.ServiceFramework):

    _svc_name_ = 'Server-Watchdog Agent'
    _svc_display_name_ = 'Server-Watchdog Agent'

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.service_impl.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        self.service_impl = MyService()
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        # Run the service
        self.service_impl.run()


def init():
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MyServiceFramework)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MyServiceFramework)


if __name__ == '__main__':
    init()
    

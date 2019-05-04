# This sample uses https://pypi.python.org/pypi/zeroconf
# as its MDNS implementation

from zeroconf import ServiceBrowser, Zeroconf
import socket
import threading
import time

class DeviceID(object):
    # Drones
    BEBOP_DRONE = '0901'
    JUMPING_SUMO = '0902'
    JUMPING_NIGHT = '0905'
    JUMPING_RACE = '0906'
    BEBOP_2 = '090c'
    MAMBO = '090b'
    DISCO = '090e'
    ANAFI = '0914'

    # Remote controllers
    SKYCONTROLLER = '0903'
    SKYCONTROLLER_2 = '090f'
    SKYCONTROLLER_2P = '0915'
    SKYCONTROLLER_3 = '0918'

    BEBOP_FAMILY = [
        BEBOP_DRONE,
        BEBOP_2,
        DISCO,
    ]

    ANAFI_FAMILY = [
        ANAFI,
    ]

    JUMPING_FAMILY = [
        JUMPING_SUMO,
        JUMPING_NIGHT,
        JUMPING_RACE,
    ]

    MAMBO_FAMILY = [
        MAMBO,
    ]

    DRONES = BEBOP_FAMILY + ANAFI_FAMILY + JUMPING_FAMILY + MAMBO_FAMILY

    REMOTES = [
        SKYCONTROLLER,
        SKYCONTROLLER_2,
        SKYCONTROLLER_2P,
        SKYCONTROLLER_3
    ]

    ALL = DRONES + REMOTES


class Discovery(object):
    """
    Basic implementation of a MDNS search for ARSDK Devices.

    The protocol here is not covered by the ARSDK but this implementation is
    here to provide a fully working sample code.
    """

    def __init__(self, deviceId):
        """
        Create and start a researcher for devices on network.

        Arguments:
        - deviceId : List of deviceIds (strings) to search.
        """
        self._deviceId=deviceId
        self._zeroconf = None
        self._browser = []
        self._services = {}

    def start(self):
        self._start=time.time()
        self._zeroconf=Zeroconf()
        self._browser = []
        self._services = {}
        for did in self._deviceId:
            b='_arsdk-' + str(did) + '._udp.local.'
            s=ServiceBrowser(self._zeroconf,b,self)
            self._browser.append(s)
           
    def stop(self):
        """
        Stop searching.

        When stopped, this object can not be restarted
        """
        # with self._lock:
        #     self._cond.notify_all()
        self._zeroconf.close()

    def get_devices(self):
        """ Get the current list of devices """
        return dict(self._services)

    def wait_for_change(self, timeout=None):
        """
        Wait for a change in the device list

        Keyword arguments:
        - timeout : Timeout in floating point seconds for the operation
        """
        # with self._lock:
        #     self._cond.wait(timeout)
        while(time.time()-self._start<timeout):
            time.sleep(1)

    def remove_service(self, zeroconf, type, name):
        """ Internal function for zeroconf.ServiceBrowser. """
        if name in self._services:
            del self._services[name]
            self._signal_change()

    def add_service(self, zeroconf, type, name):
        """ Internal function for zeroconf.ServiceBrowser. """
        info = zeroconf.get_service_info(type, name)
        # print("/////////////////////////////////////////")
        # print(name)
        # print(info)
        if info is not None:
            n=name[0:-(len(type) + 1)]
            self._services[n] = info
#            self._signal_change()
        else:
            print('Found a service witout info : ' + name + '. Stopping !')
            self.stop()
        return info

def get_name(device):
    """ Get the display name of a device """
    return device.name[0:-(len(device.type) + 1)]


def get_ip(device):
    """ Get the IP, as string, of a device """
    return socket.inet_ntoa(device.address)


def get_port(device):
    """ Get the port, as string, of a device """
    return str(device.port)


def get_device_id(device):
    """ Get the device_id of a device """
    return device.type[len('_arsdk-'):-len('._udp.local.')]

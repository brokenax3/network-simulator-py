from random import randint
import envs
from helpers import calcDistance
from helpers import calcPowerTransmit

class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def info(self):
        print("X: [{}] Y: [{}]".format(self.x, self.y))

class AccessPoint:

    def __init__(self, id, location, energy_start):
        """ Initialise an Access Point with a unique id and an empty User list. 

        Provide the Access Point with a Location within the grid. 
        Assign starting energy to the Access Point.
        Energy consumption when initialised is 0.

        If the Access Point has enough energy, set state = 1.
        """
        self.id = id
        self.location = location
        self.energy_store = energy_start
        self.energy_use = 0

        """ ap_userlist item
        List of connected Users and the distance between the User and the Access Point.

        ap_userlist[i][0] : Unique identification of the User
        ap_userlist[i][1] : Distance between the User and the Access Point
        """
        self.ap_userlist = []

        if self.energy_store >= envs.ENERGY_USE_BASE:
            self.state = 1
        else:
            self.state = 0

    def charge(self, energy_gen):
        """ Charges the Access Point 
        
        Energy generated is added into the energy_store of the Access Point.
        This is limited by ENERGY_STORE_MAX.

        TODO : Store some meaningful metric about how often energy saturation is acheived.
        """
        if self.energy_store + energy_gen >= ENERGY_STORE_MAX:
            self.energy_store = ENERGY_STORE_MAX
        else:
            self.energy_store = self.energy_store + energy_gen

    def discharge(self):
        """ Discharges the Access Point

        Energy is deducted from the Access Point energy storage.
        """
        self.energy_consumed = self.calcEnergyUse()
        self.energy_store = self.energy_store - self.energy_consumed

    def calcEnergyUse(self):
        """ Return the total energy consumption of the Access Point

        Iterates each User in self.ap_userlist and calls calcPowerTransmit with 
        the Access Point <-> User distance.
        """
        for user in self.ap_userlist:
            energy_consumed = energy_consumed + calcPowerTransmit(user[1])

        return energy_consumed

    def connectUser(self, id, distance):
        """ Connects a User to the Access Point

        If the Access Point cannot handle the User. It will reject the User.
        Updates energy consumption of the Access Point to prevent many Users connecting.
        """
        energy_use = energy_use + calcPowerTransmit(distance)

        if energy_use >= self.energy_store:
            return -1
        else:
            user = [id, distance]
            self.ap_userlist.append(user)
            self.energy_use = energy_use
            return 1

    def disconnnectUser(self):
        """ Disconnects a User from the Access Point

        """

    def stateSwitch(self):
        """ Handle the state of the Access Point

        Switch on the Access Point if there is sufficient energy to service Users.
        """
        if self.energy_store >= self.energy_use:
            self.state = 1
        else:
            self.state = 0








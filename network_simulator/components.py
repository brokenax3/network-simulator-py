from random import randint
from operator import itemgetter
from . import envs
from .helpers import calcDistance
from .helpers import calcPowerTransmit
from .discreteMarkov import energyArrivalStates
from .discreteMarkov import energyArrivalOutput
from .poissonPointProcess import generateUsersPPP

class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

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
        self.energy_consumed = 0
        self.energy_consumed_prev = 0
        self.service_counter = 0

        """ ap_userlist item
        List of connected Users and the distance between the User and the Access Point.

        ap_userlist[i][0] : Unique identification of the User
        ap_userlist[i][1] : Distance between the User and the Access Point
        """
        self.ap_userlist = []
        self.ap_userlist_prev = []

        if self.energy_store >= envs.ENERGY_USE_BASE:
            self.state = 1
        else:
            self.state = 0

    def charge(self, energy_gen):
        """ Charges the Access Point 
        
        Energy generated is added into the energy_store of the Access Point.
        This is limited by ENERGY_STORE_MAX.

        TODO: Store some meaningful metric about how often energy saturation is acheived.
        """
        if self.energy_store + energy_gen >= ENERGY_STORE_MAX:
            self.energy_store = ENERGY_STORE_MAX
        else:
            self.energy_store = self.energy_store + energy_gen

        if self.energy_store >= self.calcEnergyUse()[0]:
            self.state = 1
            # print("Access Point {} tried to turn on.".format(self.id))
        else:
            self.state = 0

    def discharge(self):
        """ Discharges the Access Point

        Energy is deducted from the Access Point energy storage.

        Sends service_counter to the Access Point Class.
        If energy_consumed is larger than energy_store, switch the Access Point off.
        """
        self.energy_consumed_prev = self.energy_consumed
        self.ap_userlist_prev = self.ap_userlist

        self.energy_consumed, service_counter = self.calcEnergyUse()
        self.service_counter = self.service_counter + service_counter

        if self.state == 0:
            self.energy_consumed = 0
            return

        if self.energy_store - self.energy_consumed > 0:
            self.energy_store = self.energy_store - self.energy_consumed
        else:
            self.energy_store = 0
            self.state = 0

    def calcEnergyUse(self):
        """ Return the total energy consumption of the Access Point

        Iterates each User in self.ap_userlist and calls calcPowerTransmit with 
        the Access Point <-> User distance.

        service_counter increments for each User the Access Point is able to service.
        """

        energy_consumed = envs.ENERGY_USE_BASE
        service_counter = 0
        for user in self.ap_userlist:
            if self.energy_store > energy_consumed:
                energy_consumed = energy_consumed + calcPowerTransmit(user[1])
                service_counter = service_counter + 1
            else:
                break

        return energy_consumed, service_counter

    def connectUser(self, id, distance):
        """ Connects a User to the Access Point

        Access Points do not deny User connections but will only service the users
        prioritising index.
        """
        if id != None and distance != None:
            self.ap_userlist.append([id, distance])
        else:
            print("id and distance not passed")

    def disconnectUser(self):
        """ Disconnects a User from the Access Point

        When the Access Point power offs, remove the Users associated with it.
        """
        for user in self.ap_userlist:
            usrlist[user[0]].removeConnected()
        self.ap_userlist = []

        # print("Kicking users resulted in {} ".format(self.ap_userlist))

    def info(self):
        """ Prints info about the Access Point

        """
        print('AP: {} \n\tLocation: ({}, {}) \n\tEnergy Stored: {} \n\tState: {} \n\tServiced Users: {}\n\tEnergy Use: {} \n\tUser List: {}'.format(self.id, self.location.x, self.location.y, self.energy_store, self.state, self.service_counter, self.energy_consumed, self.ap_userlist_prev))

    def getLoc(self):
        return [self.location.x, self.location.y]

class User:
    def __init__(self, id, location):
        """ User Class

        Initialise unique id and location.
        connected_ap[0] : ID of Access Point which the User is connected to
        connected_ap[1] : AP <-> User distance

        A User will switch to the Access Point after every timeslot.
        """
        self.id = id
        self.location = location
        self.connected_ap = ["Not Connected", "No Distance"]

    def connectAP(self):
        """ Connect to the nearest active Access Point

        If an empty list is returned, this signifies that no Access Point is online.
        A User will not do anything.
        """

        if self.connected_ap == ["Not Connected", "No Distance"]:
            status = self.calcAPDistance()
            if not status:
                self.connected_ap = ["Not Connected", "No Distance"]
                return

            self.connected_ap = status
            apid = self.connected_ap[0][0]
            distance = self.connected_ap[0][1]
            aplist[apid].connectUser(self.id, distance)

    def calcAPDistance(self):
        """ Find the nearest Access Point

        Create a list which only consists of active Access Points.
        
        return an empty list if the list is empty otherwise the id and the distance of the
        closest Access Point is returned.
        """
        active_ap_list = [[ap.id, calcDistance(self.location.x, self.location.y, ap.location.x, ap.location.y)] for ap in aplist if ap.state == 1]

        if active_ap_list == []:
            # print("Access Points are all offline")
            return active_ap_list
        else:
            closest = min(active_ap_list, key=itemgetter(1))
            return [closest]

    # Move the user to a new location
    def moveUser(self):
        # Generate two random movement numbers
        n1 = randint(-DIST_MOVEUSER_MAX, DIST_MOVEUSER_MAX)
        n2 = randint(-DIST_MOVEUSER_MAX, DIST_MOVEUSER_MAX)

        # Store the old location
        # oldloc = self.location

        # Attempt to move the self to the new location
        # For x coordinate
        if(self.location.x + n1 > GRID_SIZE):
            self.location.x = -(GRID_SIZE - self.location.x + n1 - GRID_SIZE)
        elif(self.location.x + n1 < 0):
            self.location.x = -(self.location.x + n1)
        else:
            self.location.x = self.location.x + n1
        # For y coordinate
        if(self.location.y + n2 > GRID_SIZE):
            self.location.y = -(GRID_SIZE - self.location.y + n2 - GRID_SIZE)
        elif(self.location.y + n2 < 0):
            self.location.y = -(self.location.y + n2)
        else:
            self.location.y = self.location.y + n2

    def getLoc(self):
        return [self.location.x, self.location.y]

    def removeConnected(self):
        self.connected_ap = ["Not Connected", "No Distance"]


def initialiseEnv(init_vars, ppp):
    """ Initialise the simulation environment

    Unpack init_vars from simulator.py.
    Declare global variables and constants for simulation.

    Create aplist and usrlist.
    """

    global GRID_SIZE, ENERGY_STORE_MAX, ENERGY_GEN_MAX, AP_TOTAL, USR_TOTAL, POWER_RECEIVED_REQUIRED, DIST_MOVEUSER_MAX, TIME_MAX, PANEL_SIZE
    global usrlist, aplist, markovstates

    GRID_SIZE = init_vars["GRID_SIZE"]
    ENERGY_STORE_MAX = init_vars["ENERGY_STORE_MAX"]
    ENERGY_GEN_MAX = init_vars["ENERGY_GEN_MAX"]
    AP_TOTAL = init_vars["AP_TOTAL"]
    USR_TOTAL = init_vars["USR_TOTAL"]
    POWER_RECEIVED_REQUIRED = init_vars["POWER_RECEIVED_REQUIRED"]
    DIST_MOVEUSER_MAX = init_vars["DIST_MOVEUSER_MAX"]
    TIME_MAX = init_vars["TIME_MAX"]
    PANEL_SIZE = init_vars["PANEL_SIZE"]
    markovstates = init_vars["markov"]

    aplist = [AccessPoint(index, Location(randint(0, GRID_SIZE), randint(0, GRID_SIZE)), randint(0, ENERGY_STORE_MAX)) for index in range(AP_TOTAL)]

    if ppp == 1:
        usr_x, usr_y = generateUsersPPP(GRID_SIZE, USR_TOTAL / GRID_SIZE / GRID_SIZE)

        usrlist = [User(i, Location(usr_x[i], usr_y[i])) for i in range(len(usr_x))]
    else:
        usrlist = [User(index, Location(randint(0, GRID_SIZE), randint(0, GRID_SIZE))) for index in range(USR_TOTAL)]

    # Create Markov states
    # markovstates = energyArrivalStates(TIME_MAX)

def simulator(init_vars, apuserplot, ppp):
    """ Main simulator loop

    returns the total number of clients serviced
    """

    initialiseEnv(init_vars, ppp)

    for time_unit in range(0, TIME_MAX):
        if time_unit == 0:
                continue

        for user in usrlist:
            user.moveUser()
            user.connectAP()

        for ap in aplist:
            ap.discharge()
            ap.disconnectUser()
            # ap.info()
            tmpenergy = energyArrivalOutput(markovstates[time_unit]) * PANEL_SIZE * 0.2 / 300 / 60 * 5

            # print('Energy Generated: {}'.format(tmpenergy))
            ap.charge(tmpenergy if tmpenergy < 0 else 0)

    if apuserplot == 1:
        aploc = map(AccessPoint.getLoc, aplist)
        usrloc = map(User.getLoc, usrlist)
    else:
        aploc = 0
        usrloc = 0

    # sim_service_counter = sum([ap.service_counter for ap in aplist])
    return [aploc, usrloc, sum([ap.service_counter for ap in aplist])] if apuserplot == 1 else sum([ap.service_counter for ap in aplist])

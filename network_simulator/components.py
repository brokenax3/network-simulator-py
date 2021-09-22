from random import randint
from copy import deepcopy
from operator import itemgetter
from . import envs
from .helpers import calcDistance
from .discreteMarkov import energyArrivalOutput
from .energyPolicy import energyPolicy
from .energyDistribution import energyDistributeSel

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
        # Non zero energy consumption
        self.energy_consumed_prev_nz = 0
        self.service_counter = 0

        # Logging
        self.data_energyarrival = []
        self.data_energyuse = []
        self.data_serviced_users = []
        self.data_energy_shared = []

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

        if self.energy_store >= self.energy_consumed_prev:
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
        self.ap_userlist_prev = self.ap_userlist

        if self.state == 1:
            self.energy_consumed_prev = self.energy_consumed
            [energy_consumed, serviced_users] = energyPolicy(ENERGY_POLICY, self.ap_userlist, self.energy_store)

            self.energy_consumed = energy_consumed
            self.service_counter = self.service_counter + serviced_users

            # Log additional users serviced in each timeslot
            self.data_serviced_users.append(serviced_users)
            if energy_consumed >= self.energy_store:
                self.energy_store = 0
                self.state = 0
            else:
                self.energy_store = self.energy_store - energy_consumed
        else:
            self.energy_consumed = 0

    def connectUser(self, id, distance):
        """ Connects a User to the Access Point

        Access Points do not deny User connections but will only service the users
        prioritising index.
        """
        if id != None and distance != None:
            self.ap_userlist.append([id, distance])
        else:
            print("id and distance not passed")

    def disconnectUser(self, usrlist):
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

    def connectAP(self, aplist):
        """ Connect to the nearest active Access Point

        If an empty list is returned, this signifies that no Access Point is online.
        A User will not do anything.
        """

        if self.connected_ap == ["Not Connected", "No Distance"]:
            status = self.calcAPDistance(aplist)
            if not status:
                self.connected_ap = ["Not Connected", "No Distance"]
                return

            if LOAD_BALANCE == 1:
                for item in status:
                    apid = item[0]
                    distance = item[1]
                    

                    if len(aplist[apid].ap_userlist) <= USR_LIMIT:
                        aplist[apid].connectUser(self.id, distance)
                        self.connected_ap = [apid, distance]
                        break
            else:
                apid = status[0][0]
                distance = status[0][1]

                self.connected_ap = [apid, distance]
                aplist[apid].connectUser(self.id, distance)


    def calcAPDistance(self, aplist):
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
            active_ap_list_sorted = sorted(active_ap_list, key=itemgetter(1))
            return active_ap_list_sorted

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


def initialiseEnv(init_vars):
    """ Initialise the simulation environment

    Unpack init_vars from simulator.py.
    Declare global variables and constants for simulation.

    Create aplist and usrlist.
    """

    global GRID_SIZE, ENERGY_STORE_MAX, ENERGY_GEN_MAX, AP_TOTAL, USR_TOTAL, POWER_RECEIVED_REQUIRED, DIST_MOVEUSER_MAX, TIME_MAX, PANEL_SIZE, USR_LIMIT
    global ENERGY_POLICY, SHARE_ENERGY, LOAD_BALANCE, ENERGY_BUDGET, SMART_PARAM
    global markovstates, descendunit_arr

    GRID_SIZE = init_vars["GRID_SIZE"]
    ENERGY_STORE_MAX = init_vars["ENERGY_STORE_MAX"]
    ENERGY_GEN_MAX = init_vars["ENERGY_GEN_MAX"]
    AP_TOTAL = init_vars["AP_TOTAL"]
    USR_TOTAL = init_vars["USR_TOTAL"]
    POWER_RECEIVED_REQUIRED = init_vars["POWER_RECEIVED_REQUIRED"]
    DIST_MOVEUSER_MAX = init_vars["DIST_MOVEUSER_MAX"]
    TIME_MAX = init_vars["TIME_MAX"]
    PANEL_SIZE = init_vars["PANEL_SIZE"]
    ENERGY_POLICY = init_vars["ENERGY_POLICY"]
    SHARE_ENERGY = init_vars["SHARE_ENERGY"]
    LOAD_BALANCE = init_vars["LOAD_BALANCE"]
    USR_LIMIT = init_vars["USR_LIMIT"]
    ENERGY_BUDGET = init_vars["ENERGY_BUDGET"]
    SMART_PARAM = init_vars["SMART_PARAM"]


    markovstates = init_vars["markov"]
    descendunit_arr = init_vars["descendunit_arr"]

    # Create Markov states
    # markovstates = energyArrivalStates(TIME_MAX)

def simulator(init_vars, in_aplist, in_usrlist):
    """ Main simulator loop

    returns the total number of clients serviced
    """
    # global usrlist, aplist
    usrlist = deepcopy(in_usrlist)
    aplist = deepcopy(in_aplist)

    initialiseEnv(init_vars)
    service_count = []

    for time_unit in range(0, TIME_MAX + 1):
        if time_unit == 0:
            continue

        for user in usrlist:
            user.moveUser()
            user.connectAP(aplist)

        for ap in aplist:
            ap.discharge()
            # ap.info()
            ap.disconnectUser(usrlist)
            tmpenergy = energyArrivalOutput(markovstates[time_unit])[0] * PANEL_SIZE * 0.8 * 0.001 * 60 * 5
            # print('Energy Generated: {}'.format(tmpenergy))
            ap.charge(tmpenergy if tmpenergy > 0 else 0)

            # Logging
            ap.data_energyuse.append(ap.energy_consumed)
            ap.data_energyarrival.append(tmpenergy if tmpenergy > 0 else 0)

        if SHARE_ENERGY > 0 and ENERGY_BUDGET > 0:

            energybudget_list = []
            # Allocate Energy Sharing Budget
            for ap in aplist:
                energybudget = ap.energy_store * ENERGY_BUDGET
                energybudget_list.append(energybudget)
                ap.energy_store = ap.energy_store - energybudget

                # Logging
                ap.data_energy_shared.append(energybudget)
            
            energydistributed = energyDistributeSel(aplist, SHARE_ENERGY, descendunit_arr, energybudget_list, SMART_PARAM, time_unit)

            for i, ap in enumerate(aplist):
                # ap.energy_store = 0
                tmpdistenergy = energydistributed[i][1]
                # print(tmpdistenergy)
                ap.energy_store = ap.energy_store + tmpdistenergy

    [service_count.append(ap.service_counter) for ap in aplist]

    return sum(service_count)

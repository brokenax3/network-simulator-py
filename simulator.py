#######################################################################
#                        Simulator for ECTE457                        #
#######################################################################
import numpy
from math import sqrt
from random import randint, uniform
import matplotlib.pyplot as plt



# Global AP and users
aplist = []
usrlist = []

# Class definition for Location in x and y coordinates
class Location:
    def __init__(self, x, y):

        self.x = x
        self.y = y

    def info(self):
        return "{},{}".format(self.x, self.y)

# User class to store location and identify each user
class User:
    def __init__(self, userid, location):

        # User identification
        self.userid = userid
        # Coordinate of the user
        self.location = location
        self.myap = None
        self.connected = 0
        self.dist_toAP_list = []
        self.dist_toAP = None

    # Find the distance between the user and all APs
    def findAPDist(self):
        global aplist

        # Initialise empty distance index
        dist = []

        for ap in aplist:
            if(ap.state == 1):
                dist.append([ap.apid, calcDistance(self.location.x, self.location.y, ap.location.x, ap.location.y)])

        self.dist_toAP_list = dist

    # Connect the user to the AP
    def connectAP(self):
        global aplist

        # Associate with the AP if the user is not connected
        if(self.connected == 0):
            targetAP = None

            self.findAPDist()

            while(targetAP == None):
                distance = []

                if(self.dist_toAP_list == []):
                    print("Unable to connect. All APs offline")
                    return

                for item in self.dist_toAP_list:
                    distance.append(item[1])

                for item in self.dist_toAP_list:
                    if(item[1] == min(distance)):
                        AP_min_distance = item

                # Connect to AP only when AP is active
                if(aplist[AP_min_distance[0]].state == 1 and (self.userid not in aplist[AP_min_distance[0]].userlist)):
                    targetAP = AP_min_distance[0]
                    self.myap = AP_min_distance[0]
                    self.dist_toAP =  AP_min_distance[1]
                    aplist[AP_min_distance[0]].addUser(self.userid)
                    self.connected = 1

    # Check association
    def checkConnect(self):
        global aplist

        if(self.myap != None):

            # Clear association with the AP if disconnected
            if(self.userid not in aplist[self.myap].userlist):
                self.myap = None
                self.dist_toAP = None
                self.connected = 0

    def info(self):
        print("UID: {} Coordinate: {},{} Connected: {} AP: {} Distance from AP: {}".format(self.userid, self.location.x, self.location.y, self.connected, self.myap, self.dist_toAP))

# Class definition for AP
class AccessPoint:
    def __init__(self, apid, location, energy, state):

        self.apid = apid
        # coordinate of an ap
        self.location = location
        # energy of the ap
        self.energy = energy
        # energy consumption of ap
        self.energyuse = 0
        # User list
        self.userlist = []
        # Indicate if the AP is active
        self.state = state
        self.serviceduser = 0

    def info(self):
        print("ID: {} \nEnergy: {} \nEnergy Use: {} \nState: {} \nCoordinate: ({},{}) \nUsers: {}".format(self.apid, self.energy, self.energyuse, self.state, self.location.x, self.location.y, self.userlist))

    def listUser(self):
        print(self.userlist)

    def addUser(self, item):
        self.userlist.append(item)
    
    def charge(self, energy):
        # print("Energy = {} + {}".format(self.energy, energy))
        if(self.energy + energy >= energy_store_max):
            # Extra energy will be lost
            self.energy = energy_store_max
        else:
            self.energy = self.energy + energy

        # Turn the AP on when there is energy
        if(self.state == 0 and self.energy > energy_use_base):
            self.state = 1

    def discharge(self):
        # Energy is not used when powered off
        if(self.state == 0):
            return

        # Update total energy usage
        self.energyuse = self.calcEnergyUse()

        if(self.energy - self.energyuse <= energy_use_base):
            if(self.energy - self.energyuse <= 0):
                self.energy = 0
            self.state = 0
            self.energyuse = 0
        else:
            self.energy = self.energy - self.energyuse
            # If the AP is not turned off in an iteration, count the number of users serviced
            self.serviceduser = self.serviceduser + len(self.userlist)

        # If the AP does not have enough energy to service users in the next iteration, kick a user
        while self.calcEnergyUse() > self.energy:

            if(self.userlist == []):
                break
            self.kickUser()

        # Turn the AP on when there is energy
        if(self.state == 0 and self.energy > energy_use_base):
            self.state = 1
            self.energyuse = self.calcEnergyUse()

        if(self.state == 0):
            self.energyuse = 0

    # Kick the most recently connected user if the energy consumption exceeds available energy
    def kickUser(self):

        item = self.userlist.pop()
        # print("AP [{}] kicked user {}".format(self.apid, item))

    # Calculates energy consumption based on user power consumption
    def calcEnergyUse(self):
        global usrlist

        energyuse = energy_use_base

        for user in self.userlist:
            energyuse += calcPowerTransmit(usrlist[user])

        return energyuse

# Distance between two points
def calcDistance(x1, y1, x2, y2):
    return sqrt(pow((x1 - x2),2) + pow((y1 - y2),2))

def calcPowerTransmit(user):
        # P_r is the required recieved power at a user
        # Channel Gain is 1/(d^alpha)
        # d is the distance between AP and user
        # alpha is the path loss exponent from 2 to 4

        if(user.dist_toAP == None):
            return 0
        
        d = user.dist_toAP
        alpha = 2
        # alpha = uniform(2,4)

        Pu = power_received_required * (pow(d, alpha)) * 60 * 60

        # returns transmit power in Watts
        return Pu

# Move the user to a new location
def moveUser(user):
    # Generate two random movement numbers
    n1 = randint(-dist_mvusr_max, dist_mvusr_max)
    n2 = randint(-dist_mvusr_max, dist_mvusr_max)

    # Store the old location
    oldloc = user.location.info()

    # Attempt to move the user to the new location
    # For x coordinate
    if(user.location.x + n1 > grid_size):
        user.location.x = -(grid_size - user.location.x + n1 - grid_size)
    elif(user.location.x + n1 < 0):
        user.location.x = -(user.location.x + n1)
    else:
        user.location.x = user.location.x + n1
    # For y coordinate
    if(user.location.y + n2 > grid_size):
        user.location.y = -(grid_size - user.location.y + n2 - grid_size)
    elif(user.location.y + n2 < 0):
        user.location.y = -(user.location.y + n2)
    else:
        user.location.y = user.location.y + n2

    # print("User [{}] moved to {} from {} with movement [n1:{},n2:{}]".format(user.userid, user.location.info(), oldloc, n1, n2))

# Environment building
def initialiseEnv():

    # Initialise starting parameters
    global aplist
    global usrlist
    aplist = []
    usrlist = []

    # Initialise APs
    for i in range(ap_total):

        tmploc = Location(randint(0, grid_size), randint(0, grid_size))
        tmpenergy = randint(0, energy_store_max)
        aplist.append(AccessPoint(i, tmploc, tmpenergy, 1))

    # Initialise Users
    for i in range(usr_total):

        tmploc = Location(randint(0, grid_size), randint(0, grid_size))
        usrlist.append(User(i, tmploc))

# Main simulation
def main():
    global usrlist, aplist

    serviceduser = [0] * (time_max + 1)

    # Start the simulation
    for t in range(0,time_max + 1):
        # print("""\n
#######################################################################
#                            Iteration {}                             #
#######################################################################""".format(t))
        
        # AP Discharging
        for ap in aplist:

            if(t >= 1):
                ap.discharge()

            if(t > 1):
                # Energy not harvested in the first iteration
                tmpenergy = randint(0, energy_gen_max)
                ap.charge(tmpenergy)


            # Show information about the AP
            # print("\n### AP [{}] ### ".format(ap.apid))
            # ap.info()

            # Data on serviced users
            if(ap.userlist != []):
                serviceduser[t] = serviceduser[t] + len(ap.userlist)

        # User management
        # Move users
        # print("\n### User Information ###")
        for usr in usrlist:
            usr.checkConnect()
            usr.connectAP()
            # usr.info()
            moveUser(usr)
        
    return serviceduser
    
if __name__ == "__main__":

    # Fixed Parameters for the simulator
    ap_total = 10
    # usr_total = 100 
    grid_size = 100
    energy_gen_max = 5 # Watt per hour
    dist_mvusr_max = 10
    energy_store_max = 100 # 10kWh
    energy_use_base = 5.3 # Watt
    time_max = 100
    power_received_required = 0.00001 * pow(10 ,-3) # 0.00001 mW

    serviceduser_total = numpy.zeros(100)

    for total in range(1,100):
        usr_total = total
        # Initialise the environment
        initialiseEnv()

        serviceduser = main()
        print(sum(serviceduser))
        
        # Simulation
        serviceduser_total[total] = sum(serviceduser)

    # initialiseEnv()
    # main()
    # Plotting
    plt.plot(range(1, 101), serviceduser_total)
    plt.show()

    

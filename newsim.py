# Simulator for ECTE457
from random import randint, uniform
from math import sqrt
import matplotlib.pyplot as plt

# Definition of a Location item
class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def info(self):
        print("X: [{}] Y: [{}]".format(self.x, self.y))

# Definition for an Access Point item
class AccessPoint:
    def __init__(self, apid, location, energy_start):
        self.apid = apid
        self.location = location
        self.energy_store = energy_start
        self.energy_use = 0
        self.ap_usrlist = []
        if self.energy_store >= energy_use_base:
            self.state = 1
        else:
            self.state = 0
        self.serviced_user_n = 0
        self.kicklist = []

    def info(self):
        print('AP: {} \n\tLocation: ({}, {}) \n\tEnergy Stored: {} \n\tState: {} \n\tEnergy Use: {} \n\tUser List: {}'.format(self.apid, self.location.x, self.location.y, self.energy_store, self.state, self.energy_use, self.ap_usrlist))

    # Energy generation at the Access Point
    def charge(self, energy_gen):
        if self.energy_store + energy_gen >= energy_store_max:
            # Access Point fully charged
            self.energy_store = energy_store_max
        else:
            # Store energy in the Access Point
            self.energy_store = self.energy_store + energy_gen

        if self.energy_store > self.calcEnergyUse():
            self.state = 1

    def discharge(self):
        self.energy_use = self.calcEnergyUse()

        # Energy is not used when AP is powered off
        if self.state == 0:
            self.energy_use == 0
            return

        # print(self.energy_use)
        # print(self.energy_store)
        # print(self.ap_usrlist)

        if self.energy_store - self.energy_use <= 0:
            self.energy_store = 0
            self.state = 0
            self.energy_use = 0
        else:
            self.energy_store = self.energy_store - self.energy_use
            self.serviced_user_n = self.serviced_user_n + len(self.ap_usrlist)

    def connectUser(self, userid):
        self.ap_usrlist.append(userid)

    def disconnectUser(self):
        if self.ap_usrlist == [] and self.state == 0:
            self.energy_use = 0
            return
        # Find the energy required to sustain the next time slot
        kicklist = []
        energy_use = self.calcEnergyUse()

        while energy_use > self.energy_store + energy_use_base:
            energy_use = self.calcEnergyUse()
            if self.ap_usrlist == []:
                self.energy_use = 0
                break
            # Save the users to be disconnected at the start of the next time slot
            user = self.ap_usrlist.pop()
            usrlist[user].checkConnect()
            kicklist.append(user)
            # Update Energy Use for display
            self.energy_use = self.calcEnergyUse()

        self.kicklist = kicklist

    # Calculate the total energy use
    def calcEnergyUse(self):
        energy_use = energy_use_base
        # Calculate the total energy use
        for user in self.ap_usrlist:
            energy_use = energy_use + calcPowerTransmit(usrlist[user])
        
        return energy_use

# Definition of a User item
class User:
    def __init__(self, userid, location):
        self.userid = userid
        self.location = location
        self.connected = 0
        self.connected_ap = "Not Connected"
        self.connected_ap_dist = "Not Connected"

    def info(self):
        print('User: {} \n\tLocation: ({}, {}) \n\tConnected to AP: {} \n\tConnected: {} \n\tDistance: {}'.format(self.userid, self.location.x, self.location.y, self.connected, self.connected_ap, self.connected_ap_dist))

    def findAPDist(self):
        # Empty distance array for where the user currently is to all the APs
        AP_Dist_arr = []
        distances = []
        for ap in aplist:
            # Only take Online APs
            if ap.state == 1:
                AP_Dist_arr.append([ap.apid, calcDistance(self.location.x, self.location.y, ap.location.x, ap.location.y)])

        if not AP_Dist_arr:
            return AP_Dist_arr
        else:
            # Find the smallest distance within the online APs
            for dist in AP_Dist_arr:
                distances.append(dist[1])
            # Return the id and distance of the AP
            for item in AP_Dist_arr:
                if item[1] == min(distances):
                    return item

    def connectAP(self):
        # Associate with an Access Point if User is not connected
        # if self.connected == 0:
        # Get the AP with the smallest distance from the User
        status = self.findAPDist()

        if not status:
            print('APs Offline')
            self.connected = 0
            self.connected_ap = 'Not Connected'
            self.connected_ap_dist = 'Not Connected'
        else:
            self.connected_ap = status[0]
            self.connected_ap_dist = status[1]
            aplist[self.connected_ap].connectUser(self.userid)
            self.connected = 1

    def checkConnect(self):
        self.connected = 0
        self.connected_ap = 'Not Connected'
        self.connected_ap_dist = 'Not Connected'

# Distance between two points
def calcDistance(x1, y1, x2, y2):
    return sqrt(pow((x1 - x2),2) + pow((y1 - y2),2))

def calcPowerTransmit(user):
        # P_r is the required recieved power at a user
        # Channel Gain is 1/(d^alpha)
        # d is the distance between AP and user
        # alpha is the path loss exponent from 2 to 4
    if user.connected_ap != 'Not Connected':
        d = user.connected_ap_dist
        alpha = uniform(2,4)
        Pu = power_received_required * (pow(d, alpha)) * 60
        # returns transmit power in Watts
        return Pu
    else:
        return 0

# Move the user to a new location
def moveUser(user):
    # Generate two random movement numbers
    n1 = randint(-dist_moveuser_max, dist_moveuser_max)
    n2 = randint(-dist_moveuser_max, dist_moveuser_max)

    # Store the old location
    oldloc = user.location

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

    # Initialise Access Points
    for index in range(ap_total):
        tmploc = Location(randint(0, grid_size), randint(0, grid_size))
        tmpenergy = randint(0, energy_store_max)
        tmpap = AccessPoint(index, tmploc, tmpenergy)
        aplist.append(tmpap)

    # Initialise Users
    for index in range(usr_total):
        tmploc = Location(randint(0, grid_size), randint(0, grid_size))
        tmpusr = User(index, tmploc) 
        usrlist.append(tmpusr)

def simulator():
    serviced_user_sim = 0 

    for time in range(0, time_max):
        # print('\n' + '#'*40)
        # print('Time Slot: {}'.format(time))
        # print('#'*40)

        if time == 0:
            for ap in aplist:
                # ap.info()
                continue

        for user in usrlist:
            moveUser(user)
            user.connectAP()

        for ap in aplist:
            ap.discharge()
            ap.disconnectUser()
            # ap.info()
            tmpenergy = randint(0, energy_gen_max)
            # print('Energy Generated: {}'.format(tmpenergy))
            ap.charge(tmpenergy)

    for ap in aplist:
        serviced_user_sim = serviced_user_sim + ap.serviced_user_n
    
    return serviced_user_sim

def initVariable():
    global grid_size, energy_store_max, energy_gen_max, energy_use_base, ap_total, usr_total, power_received_required, time_max, usrlist, aplist, dist_moveuser_max

    # Define starting variables
    grid_size = 30
    energy_store_max = 500      # 1kWh battery
    energy_gen_max = 5          # Watt per hour
    energy_use_base = 5.3
    ap_total = 5
    usr_total = 15
    power_received_dbm = -70 
    power_received_required = 1 * pow(10, power_received_dbm/10)
    time_max = 1440 # Minutes for a day
    dist_moveuser_max = 5

    # Define the users and access points
    usrlist = []
    aplist = []

if __name__ == '__main__':

    # Create empty lists to store collected data
    serviced_user_sim_arr_usernumber = []
    serviced_user_sim_arr_apnumber = []
    serviced_user_sim_arr_energyarrival = []
    serviced_user_sim_arr_usermovedist = []
    serviced_user_sim_arr_gridsize = []
    serviced_user_sim_arr_userenergyuse = []
    serviced_user_sim_arr_energystore = []
    
    #######################
    #  Simulator Section  #
    #######################
    # Number of Access Points
    initVariable()
    range_AP_total = range(1, 30, 5)
    for ap_total in range_AP_total:
        initialiseEnv()
        serviced_user_sim_arr_apnumber.append(simulator())

    # Number of Users
    initVariable()
    range_usr_total = range(1, 30, 5)
    for usr_total in range_usr_total:
        initialiseEnv()
        serviced_user_sim_arr_usernumber.append(simulator())

    # Energy Arrival
    initVariable()
    range_energy_gen_max = range(1, 10)
    for energy_gen_max in range_energy_gen_max:
        initialiseEnv()
        serviced_user_sim_arr_energyarrival.append(simulator())

    # Distance moved by user
    initVariable()
    range_dist_moveuser_max = range(1, 15)
    for dist_moveuser_max in range_dist_moveuser_max:
        initialiseEnv()
        serviced_user_sim_arr_usermovedist.append(simulator())

    # Grid Size
    initVariable()
    range_grid_size = range(10, 100, 10)
    for grid_size in range_grid_size:
        initialiseEnv()
        serviced_user_sim_arr_gridsize.append(simulator())

    # User minimum received power required
    initVariable()
    range_power_received_dbm = range(-80, -30, 2)
    for power_received_dbm in range_power_received_dbm:
        initialiseEnv()
        serviced_user_sim_arr_userenergyuse.append(simulator())

    # Energy storeage
    initVariable()
    range_energy_store_max = range(100, 1000, 100)
    for energy_store_max in range_energy_store_max:
        initialiseEnv()
        serviced_user_sim_arr_energystore.append(simulator())

    ##############
    #  Plotting  #
    ##############
    ap_x = []
    ap_y = []
    usr_x = []
    usr_y = []

    for ap in aplist:
        ap_x.append(ap.location.x)
        ap_y.append(ap.location.y)

    for user in usrlist:
        usr_x.append(user.location.x)
        usr_y.append(user.location.y)

    plt.rcParams["font.family"] = "Iosevka SS16"
    plot1 = plt.figure(1)
    plt.scatter(ap_x, ap_y, label='Access Points', color='red', marker='*')
    plt.scatter(usr_x, usr_y, label='Users', color='blue', marker='o')
    plt.xlabel('x - axis')
    plt.ylabel('y - axis')
    plt.title('Coordinate of APs and Users in the Grid')
    plt.legend()
    plt.savefig('scatterAPUser.png')

    plot2 = plt.figure(2)
    plt.plot(range_AP_total, serviced_user_sim_arr_apnumber)
    plt.xlabel('Total Number of APs')
    plt.ylabel('Total Number of Serviced Users')
    plt.title('Total Number of APs against Total Number of Serviced users')
    plt.savefig('totalnumberap.png')

    plot3 = plt.figure(3)
    plt.plot(range_usr_total, serviced_user_sim_arr_usernumber)
    plt.xlabel('Total Number of Users')
    plt.ylabel('Total Number of Serviced Users')
    plt.title('Total Number of Users against Total Number of Serviced users')
    plt.savefig('totalnumberuser.png')

    plot4 = plt.figure(4)
    plt.plot(range_energy_gen_max, serviced_user_sim_arr_energyarrival)
    plt.xlabel('Maximum Energy Arrival')
    plt.ylabel('Total Number of Serviced Users')
    plt.title('Maximum Energy Arrival against Total Number of Serviced users')
    plt.savefig('maxenergyarrival.png')

    plot5 = plt.figure(5)
    plt.plot(range_dist_moveuser_max, serviced_user_sim_arr_usermovedist)
    plt.xlabel('Maximum User Movement Distance')
    plt.ylabel('Total Number of Serviced Users')
    plt.title('Maximum User Movement Distance against Total Number of Serviced users')
    plt.savefig('maxusermove.png')

    plot6 = plt.figure(6)
    plt.plot(range_grid_size, serviced_user_sim_arr_gridsize)
    plt.xlabel('Grid Size')
    plt.ylabel('Total Number of Serviced Users')
    plt.title('Grid Size against Total Number of Serviced users')
    plt.savefig('gridsize.png')

    plot7 = plt.figure(7)
    plt.plot(range_power_received_dbm, serviced_user_sim_arr_userenergyuse)
    plt.xlabel('Minimum Received Power')
    plt.ylabel('Total Number of Serviced Users')
    plt.title('Minimum Received Power against Total Number of Serviced users')
    plt.savefig('minreceivedpower.png')

    plot8 = plt.figure(8)
    plt.plot(range_energy_store_max, serviced_user_sim_arr_energystore)
    plt.xlabel('Energy Storage Capacity')
    plt.ylabel('Total Number of Serviced Users')
    plt.title('Energy Storage Capacity against Total Number of Serviced users')
    plt.savefig('energystorage.png')
    plt.show()

# Energy Stored is after the time slot
# Energy Use is the energy used within the time slot

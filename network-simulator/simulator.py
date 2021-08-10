import matplotlib.pyplot as plt
from random import randint
from components import simulator
from progress.bar import Bar

def initVariable():
    """ Initilise starting variables

    A dict is generated and modified as needed. This modified dict is passed into the simulator.
    Time unit 5 minutes.
    """

    init_vars = {
        "GRID_SIZE" : 30,
        "ENERGY_STORE_MAX" : 576, # Watt 5 minutes
        "ENERGY_GEN_MAX" : 0.75, # Watt  
        "ENERGY_USE_BASE" : 0.4417, # Watt per 5 minutes
        "AP_TOTAL" : 5,
        "USR_TOTAL" : 500,
        "POWER_RECEIVED_DBM" : -65, 
        "TIME_MAX" : 288,
        "DIST_MOVEUSER_MAX" : 5,
    }
    init_vars["POWER_RECEIVED_REQUIRED"] = 1 * pow(10, init_vars["POWER_RECEIVED_DBM"]/10) / 1000 * 60 * 5
    return init_vars

def plotGraphs():
    """ Plot graphs from the simulation

    """
if __name__ == '__main__':

    total_runs = range(1, 10)

    # Create empty lists to store collected data
    avg_serviced_user_sim_arr_apnumber = []
    # serviced_user_sim_arr_usernumber = []
    # serviced_user_sim_arr_energyarrival = []
    # serviced_user_sim_arr_usermovedist = []
    # serviced_user_sim_arr_gridsize = []
    # serviced_user_sim_arr_userenergyuse = []
    # serviced_user_sim_arr_energystore = []
    
    #######################
    #  Simulator Section  #
    #######################
    # Number of Access Points
    bar = Bar('Running simulation', max=total_runs[-1])
    for run in total_runs:
        range_AP_total = range(1, 30, 5)
        serviced_user_sim_arr_apnumber = []
        for AP_TOTAL in range_AP_total:
            init_vars = initVariable()
            init_vars["AP_TOTAL"] = AP_TOTAL
            serviced_user_sim_arr_apnumber.append(simulator(init_vars))
        avg_serviced_user_sim_arr_apnumber.append(serviced_user_sim_arr_apnumber)
        bar.next()
    bar.finish()
    sum_arr = map(sum, zip(*avg_serviced_user_sim_arr_apnumber))

    new_arr = []
    for item in sum_arr:
        new_arr.append(item / total_runs[-1] )


    # print(serviced_user_sim_arr_apnumber)

    # # Number of Users
    # range_usr_total = range(1, 30, 5)
    # for usr_total in range_usr_total:
    #     serviced_user_sim_arr_usernumber.append(simulator(initVariable()))

    # # Energy Arrival
    # range_energy_gen_max = range(1, 10)
    # for energy_gen_max in range_energy_gen_max:
    #     serviced_user_sim_arr_energyarrival.append(simulator(initVariable()))

    # # Distance moved by user
    # range_dist_moveuser_max = range(1, 15)
    # for dist_moveuser_max in range_dist_moveuser_max:
    #     serviced_user_sim_arr_usermovedist.append(simulator(initVariable()))

    # # Grid Size
    # range_grid_size = range(10, 100, 10)
    # for grid_size in range_grid_size:
    #     serviced_user_sim_arr_gridsize.append(simulator(initVariable()))

    # # User minimum received power required
    # range_power_received_dbm = range(-80, -30, 2)
    # for power_received_dbm in range_power_received_dbm:
    #     serviced_user_sim_arr_userenergyuse.append(simulator(initVariable()))

    # # Energy storeage
    # range_energy_store_max = range(100, 1000, 100)
    # for energy_store_max in range_energy_store_max:
    #     serviced_user_sim_arr_energystore.append(simulator(initVariable()))

    ##############
    #  Plotting  #
    ##############
    # ap_x = []
    # ap_y = []
    # usr_x = []
    # usr_y = []

    # for ap in aplist:
    #     ap_x.append(ap.location.x)
    #     ap_y.append(ap.location.y)

    # for user in usrlist:
    #     usr_x.append(user.location.x)
    #     usr_y.append(user.location.y)

    # plt.rcParams["font.family"] = "Iosevka SS16"
    # plot1 = plt.figure(1)
    # plt.scatter(ap_x, ap_y, label='Access Points', color='red', marker='*')
    # plt.scatter(usr_x, usr_y, label='Users', color='blue', marker='o')
    # plt.xlabel('x - axis')
    # plt.ylabel('y - axis')
    # plt.title('Coordinate of APs and Users in the Grid')
    # plt.legend()
    # plt.savefig('scatterAPUser.png')

    plot2 = plt.figure(2)
    plt.plot(range_AP_total, new_arr)
    plt.xlabel('Total Number of APs')
    plt.ylabel('Total Number of Serviced Users')
    plt.title('Total Number of APs against Total Number of Serviced users')
    plt.savefig('totalnumberap.png')

    # plot3 = plt.figure(3)
    # plt.plot(range_usr_total, serviced_user_sim_arr_usernumber)
    # plt.xlabel('Total Number of Users')
    # plt.ylabel('Total Number of Serviced Users')
    # plt.title('Total Number of Users against Total Number of Serviced users')
    # plt.savefig('totalnumberuser.png')

    # plot4 = plt.figure(4)
    # plt.plot(range_energy_gen_max, serviced_user_sim_arr_energyarrival)
    # plt.xlabel('Maximum Energy Arrival')
    # plt.ylabel('Total Number of Serviced Users')
    # plt.title('Maximum Energy Arrival against Total Number of Serviced users')
    # plt.savefig('maxenergyarrival.png')

    # plot5 = plt.figure(5)
    # plt.plot(range_dist_moveuser_max, serviced_user_sim_arr_usermovedist)
    # plt.xlabel('Maximum User Movement Distance')
    # plt.ylabel('Total Number of Serviced Users')
    # plt.title('Maximum User Movement Distance against Total Number of Serviced users')
    # plt.savefig('maxusermove.png')

    # plot6 = plt.figure(6)
    # plt.plot(range_grid_size, serviced_user_sim_arr_gridsize)
    # plt.xlabel('Grid Size')
    # plt.ylabel('Total Number of Serviced Users')
    # plt.title('Grid Size against Total Number of Serviced users')
    # plt.savefig('gridsize.png')

    # plot7 = plt.figure(7)
    # plt.plot(range_power_received_dbm, serviced_user_sim_arr_userenergyuse)
    # plt.xlabel('Minimum Received Power')
    # plt.ylabel('Total Number of Serviced Users')
    # plt.title('Minimum Received Power against Total Number of Serviced users')
    # plt.savefig('minreceivedpower.png')

    # plot8 = plt.figure(8)
    # plt.plot(range_energy_store_max, serviced_user_sim_arr_energystore)
    # plt.xlabel('Energy Storage Capacity')
    # plt.ylabel('Total Number of Serviced Users')
    # plt.title('Energy Storage Capacity against Total Number of Serviced users')
    # plt.savefig('energystorage.png')
    # plt.show()

# Energy Stored is after the time slot
# Energy Use is the energy used within the time slot
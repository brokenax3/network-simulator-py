from random import randint
import matplotlib.pyplot as plt
from network_simulator.components import simulator
from network_simulator.components import Location
from network_simulator.components import AccessPoint
from network_simulator.components import User
from network_simulator.poissonPointProcess import generateUsersPPP
from network_simulator.discreteMarkov import energyArrivalStates
from network_simulator.testPolicy import energyPolicyTest
from progress.bar import Bar

def initVariable(ppp):
    """ Initilise starting variables

    A dict is generated and modified as needed. This modified dict is passed into the simulator.
    Time unit 5 minutes.
    """

    init_vars = {
        "GRID_SIZE" : 50,
        "ENERGY_STORE_MAX" : 576, # Watt 5 minutes
        "ENERGY_GEN_MAX" : 0.75, # Watt  
        "PANEL_SIZE" : 5, # cm^2
        "ENERGY_USE_BASE" : 0.4417, # Watt per 5 minutes 5.3/60*5
        "AP_TOTAL" : 5,
        "USR_TOTAL" : 100,
        "POWER_RECEIVED_DBM" : -60, 
        "TIME_MAX" : 10000,
        "DIST_MOVEUSER_MAX" : 5,
        "ENERGY_POLICY" : 0,
        "SHARE_ENERGY" : 0,
    }
    init_vars["POWER_RECEIVED_REQUIRED"] = 1 * pow(10, init_vars["POWER_RECEIVED_DBM"]/10) * 60 * 5 * 0.001 # Watts per 5 minutes

    GRID_SIZE = init_vars["GRID_SIZE"]
    ENERGY_STORE_MAX = init_vars["ENERGY_STORE_MAX"]
    AP_TOTAL = init_vars["AP_TOTAL"]
    USR_TOTAL = init_vars["USR_TOTAL"]

    # Generate fixed User and AP list
    aplist = [AccessPoint(index, Location(randint(0, GRID_SIZE), randint(0, GRID_SIZE)), randint(0, ENERGY_STORE_MAX)) for index in range(AP_TOTAL)]

    if ppp == 1:
        usr_x, usr_y = generateUsersPPP(GRID_SIZE, USR_TOTAL / GRID_SIZE / GRID_SIZE)

        usrlist = [User(i, Location(usr_x[i], usr_y[i])) for i in range(len(usr_x))]
    else:
        usrlist = [User(index, Location(randint(0, GRID_SIZE), randint(0, GRID_SIZE))) for index in range(USR_TOTAL)]
    return init_vars, aplist, usrlist

if __name__ == '__main__':

    total_runs = range(5)

    # Create empty lists to store collected data
    tmp_serviced_user_apnumber = []
    tmp_serviced_user_usernumber = []
    tmp_serviced_user_panelsize = []
    # serviced_user_usermovedist = []
    # serviced_user_gridsize = []
    # serviced_user_userenergyuse = []
    # serviced_user_energystore = []
    
    #######################
    #  Simulator Section  #
    #######################
    init_vars, aplist, usrlist = initVariable(1)
    # Retain the same list for passing into the simulator
    tmp_init_vars = init_vars
    tmp_aplist = aplist
    tmp_usrlist = usrlist
    markovstates = energyArrivalStates(init_vars["TIME_MAX"])
    init_vars["markov"] = markovstates

    # [aploc, usrloc, serviced] = simulator(init_vars, 1, 0)
    # [aploc_ppp, usrloc_ppp, serviced] = simulator(init_vars, 1, 1)
    # Number of Access Points
    # range_AP_total = range(1, 50, 5)
    # bar = Bar('Running simulation (Number of APs)', max=len(range_AP_total))

    # for run in total_runs:
    #     serviced_user_apnumber = []
    #     for AP_TOTAL in range_AP_total:
    #         init_vars["AP_TOTAL"] = AP_TOTAL
    #         serviced_user_apnumber.append(simulator(init_vars))
    #     tmp_serviced_user_apnumber.append(serviced_user_apnumber)
    #     bar.next()
    # bar.finish()
    # avg_sum_serviced_user_apnumber = map(sum, zip(*tmp_serviced_user_apnumber))

    # avg_serviced_user_apnumber = []
    # # for item in avg_sum_serviced_user_apnumber:
    # #     avg_serviced_user_apnumber.append(item / len(total_runs))
    # for AP_TOTAL in range_AP_total:
    #     init_vars["AP_TOTAL"] = AP_TOTAL
    #     serviced_user_apnumber = [simulator(init_vars, 0, 0) for run in total_runs]
    #     avg_serviced_user_apnumber.append(sum(serviced_user_apnumber) / len(total_runs))
    #     bar.next()
    # bar.finish()

    # # Number of Users
    # bar = Bar('Running simulation (Number of Users)', max=len(total_runs))
    # for run in total_runs:
    #     range_USR_total = range(100, 1000, 100)
    #     serviced_user_usernumber = []
    #     for USR_TOTAL in range_USR_total:
    #         init_vars = initVariable()
    #         init_vars["USR_TOTAL"] = USR_TOTAL
    #         serviced_user_usernumber.append(simulator(init_vars))
    #     tmp_serviced_user_usernumber.append(serviced_user_usernumber)
    #     bar.next()
    # bar.finish()
    # avg_sum_serviced_user_usernumber = map(sum, zip(*tmp_serviced_user_usernumber))

    # avg_serviced_user_usernumber = []
    # for item in avg_sum_serviced_user_usernumber:
    #     avg_serviced_user_usernumber.append(item / len(total_runs))

    # # Energy Arrival (Changing panel size)
    # bar = Bar('Running simulation (Panel Size)', max=len(total_runs))
    # for run in total_runs:
    #     range_PANELSIZE_total = range(10)
    #     serviced_user_panelsize = []
    #     for PANEL_SIZE in range_PANELSIZE_total:
    #         init_vars = initVariable()
    #         init_vars["PANEL_SIZE"] = PANEL_SIZE
    #         serviced_user_panelsize.append(simulator(init_vars))
    #     tmp_serviced_user_panelsize.append(serviced_user_panelsize)
    #     bar.next()
    # bar.finish()
    # avg_sum_serviced_user_panelsize = map(sum, zip(*tmp_serviced_user_panelsize))

    # avg_serviced_user_panelsize = []
    # for item in avg_sum_serviced_user_panelsize:
    #     avg_serviced_user_panelsize.append(item /  len(total_runs))

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
    
    # ap_loc_x= []
    # ap_loc_y= []
    # for ap in aplist: 1.116
    #     ap_loc_x.append(ap.location.x)
    #     ap_loc_y.append(ap.location.y)

    # print(ap_arr)

    # ap_loc = list(zip(*aploc))
    # usr_loc = list(zip(*usrloc))
    
    # ap_loc_ppp = list(zip(*aploc_ppp))
    # usr_loc_ppp = list(zip(*usrloc_ppp))

    # plt.rcParams["font.family"] = "Iosevka SS16"
    # plot1 = plt.figure(1)
    # plt.scatter(ap_loc[0], ap_loc[1], label='Access Points', color='red', marker='*')
    # plt.scatter(usr_loc[0], usr_loc[1], label='Users', color='blue', marker='o')
    # plt.xlabel('x - axis')
    # plt.ylabel('y - axis')
    # plt.title('Coordinate of APs and Users in the Grid')
    # plt.legend()
    # plt.savefig('scatterAPUser.png')
    
    # PPP
    # plot2 = plt.figure(2)
    # plt.scatter(ap_loc_ppp[0], ap_loc_ppp[1], label='Access Points', color='red', marker='*')
    # plt.scatter(usr_loc_ppp[0], usr_loc_ppp[1], label='Users', color='blue', marker='o')
    # plt.xlabel('x - axis')
    # plt.ylabel('y - axis')
    # plt.title('Coordinate of APs and Users in the Grid (Poisson Point Process)')
    # plt.legend()
    # plt.savefig('scatterAPUser_ppp.png')

    # plot2 = plt.figure(2)
    # plt.plot(range_AP_total, avg_serviced_user_apnumber)
    # plt.xlabel('Total Number of APs')
    # plt.ylabel('Total Number of Serviced Users')
    # plt.title('Total Number of Serviced users against Total Number of APs')
    # plt.savefig('totalnumberap.png')

    # plot3 = plt.figure(3)
    # plt.plot(range_USR_total, avg_serviced_user_usernumber)
    # plt.xlabel('Total Number of Users')
    # plt.ylabel('Total Number of Serviced Users')
    # plt.title('Total Number of Serviced users against Total Number of Users')
    # plt.savefig('totalnumberuser.png')

    # plot4 = plt.figure(4)
    # plt.plot(range_PANELSIZE_total, avg_serviced_user_panelsize)
    # plt.xlabel('Size of Solar Panel (cm^2)')
    # plt.ylabel('Total Number of Serviced Users')
    # plt.title('Total Number of Serviced users against Size of Solar Panel')
    # plt.savefig('panelsize.png')

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

    plt = energyPolicyTest(tmp_init_vars, tmp_aplist, tmp_usrlist)
    
    plt.savefig('energypolicyppp.png')

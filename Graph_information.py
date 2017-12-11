import pandas as pd
import numpy as np


def store_information(filepath, data, number, outcome=None):
    list_of_ag = ["ag_" + str(d) for d in data['AntihypertensiveClassCombined']]
    list_of_con = ["con_" + str(d) for d in data['ConcomitantClass']]
    f = open(filepath, 'w')
    f.write("nodedef>name VARCHAR,color VARCHAR\n")
    f.close()
    f = open(filepath, 'a')
    if outcome is None:
        for i in range(number):
            if list_of_con[i] != 'con_nan':
                f.write('{},"173,255,47"\n'.format(list_of_con[i]))
        for i in range(number):
            if list_of_con[i] != 'con_nan':
                f.write('{},"0,250,154"\n'.format(list_of_ag[i]))
        f.write("edgedef>node1 VARCHAR,node2 VARCHAR\n")
        for i in range(number):
            if list_of_con[i] != 'con_nan':
                f.write('{},{}\n'.format(list_of_ag[i], list_of_con[i]))
        f.close()
    else:
        for i in range(number):
            if data['TreatmentOutcome'][i] == outcome and list_of_con[i] != 'con_nan':
                f.write('{},"173,255,47"\n'.format(list_of_con[i]))
                f.write('{},"0,250,154"\n'.format(list_of_ag[i]))
        f.write("edgedef>node1 VARCHAR,node2 VARCHAR\n")
        for i in range(number):
            if data['TreatmentOutcome'][i] == outcome and list_of_con[i] != 'con_nan':
                f.write('{},{}\n'.format(list_of_ag[i], list_of_con[i]))
        f.close()


def make_unique_data_file(path, data):
    list_single = dict()
    for d in zip(data['AntihypertensiveClassCombined'], data['ConcomitantClass'], data['TreatmentOutcome']):
        if str(d[1]) != 'nan':
            if list_single.get('ag_' + str(d[0]) + ',' + 'con_' + str(d[1])) is None:
                list_single['ag_' + str(d[0]) + ',' + 'con_' + str(d[1])] = ['ag_' + str(d[0]), 'con_' + str(d[1]), 1,
                                                                             d[2]]
            else:
                list_single['ag_' + str(d[0]) + ',' + 'con_' + str(d[1])][2:] = [
                    list_single.get('ag_' + str(d[0]) + ',' +
                                    'con_' + str(d[1]))[2] + 1,
                    list_single.get('ag_' + str(d[0]) + ',' +
                                    'con_' + str(d[1]))[3] + d[2]]
    f = open(path, 'w')
    f.write("nodedef>name VARCHAR,color VARCHAR\n")
    f.close()
    f = open(path, 'a')
    for d in list_single.keys():
        if list_single.get(d)[2] >= 20:
            f.write('{},"128,0,0"\n'.format(list_single.get(d)[0]))
            f.write('{},"0,0,128"\n'.format(list_single.get(d)[1]))
    f.write("edgedef>node1 VARCHAR,node2 VARCHAR,label VARCHAR\n")
    for d in list_single.keys():
        if list_single.get(d)[2] >= 20:
            f.write(str(d) + ',{:.2f}\n'.format(list_single.get(d)[3]/list_single.get(d)[2]))
    f.close()


data = pd.read_csv("Data_for_DecisionTreeRegressor_Add_HeartRate&ConcomitantDrugs.csv", sep=';', encoding='utf-8')
# store_information('graph_outcome_1.gdf', data, len(data), 1)
make_unique_data_file('u_20.gdf',data)


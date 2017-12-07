import pandas as pd


data = pd.read_csv("Data_for_DecisionTreeRegressor_Add_HeartRate&ConcomitantDrugs.csv", sep=';',
                          encoding='utf-8')
# data = data.dropna(subset=['ConcomitantClass','ID'], how='any')
list_of_ag = ["ag_" + str(d) for d in data['AntihypertensiveClassCombined']]
list_of_con = ["con_" + str(d) for d in data['ConcomitantClass']]
dataframe = pd.DataFrame(columns=list_of_ag, index=list_of_con)


for i in range(len(data)):
    dataframe.set_value(list_of_con[i], list_of_ag[i],
                        data['TreatmentOutcome'][i])
dataframe.to_csv("graph.csv", sep=';')
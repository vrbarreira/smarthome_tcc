from datetime import datetime as dt
import csv
import pickle

def lerCSV(arquivo, matriz):
    leitura = open(arquivo, "r").readlines()
    for linha in leitura:
        matriz.append(linha.strip().split(','))

matriz_comodo_sensores = []
matriz_atividades = []
matriz_correlacao_sensores = []
matriz_rotulos_lv1 = []
matriz_rotulos_lv2 = []

matriz_apriori = []
with open('Saidas/AprioriAllBin.txt',  'rb') as fileBin:
    matriz_apriori = pickle.load(fileBin)

lerCSV("id_comodo_sensores.csv", matriz_comodo_sensores)
lerCSV("atividades.csv", matriz_atividades)
lerCSV("correlacao_sensores.csv", matriz_correlacao_sensores)
lerCSV("Saidas/classif_results_lv1.csv", matriz_rotulos_lv1)

def filtro_correl_sensores_novo():
    mtx_aux = []
    data_inicio = '14-04-2019 00:00'
    data_fim = '27-05-2019 23:59'

    for i in range(1,len(matriz_correlacao_sensores)):
        id_sensor_1 = matriz_correlacao_sensores[i][0]
        id_sensor_2 = matriz_correlacao_sensores[i][1]

        for j in range(1,len(matriz_rotulos_lv1)):

            if j < len(matriz_rotulos_lv1)-1:
                dt_aux = dt.strptime(matriz_rotulos_lv1[j][1], '%Y-%m-%d %H:%M')

                if dt_aux >= dt.strptime(data_inicio, '%d-%m-%Y %H:%M') and dt_aux <= dt.strptime(data_fim, '%d-%m-%Y %H:%M'):
                    k = 1
                    while matriz_rotulos_lv1[j][0] == matriz_rotulos_lv1[j+k][0]:
                        if matriz_rotulos_lv1[j][0] == matriz_rotulos_lv1[j+k][0]:
                            teste1 = matriz_rotulos_lv1[j][2] == id_sensor_1 and matriz_rotulos_lv1[j+k][2] == id_sensor_2
                            teste2 = matriz_rotulos_lv1[j][4] == matriz_correlacao_sensores[i][2] and matriz_rotulos_lv1[j+k][4] == matriz_correlacao_sensores[i][2]
                            
                            if teste1 and teste2:
                                mtx_aux.append(matriz_rotulos_lv1[j])
                                mtx_aux.append(matriz_rotulos_lv1[j+k])
                        
                        
                        if j+k < len(matriz_rotulos_lv1)-1:
                            k = k+1
                        else:
                            break
        
    return mtx_aux

def filtro_correl_sensores_aprioriall():
    pass

matriz_rotulos_lv2 = filtro_correl_sensores_novo()

def sortIdx(val):
    return int(val[0])

matriz_rotulos_lv2.sort(key=sortIdx)

with open('Saidas/classif_results_lv2.csv', 'w', newline='') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerow(['Id Home', 'Timestamp', 'Sensor Comodo', 'Comodo', 'Id Atividade', 'Atividade'])
    writer.writerows(matriz_rotulos_lv2)

writeFile.close()
from datetime import datetime as dt
import csv
import pickle

def lerCSV(arquivo, matriz):
    with open(arquivo, "r") as arq:
        leitura = arq.readlines()
        for linha in leitura:
            matriz.append(linha.strip().split(','))
    arq.close()

matriz_correlacao_sensores = []
matriz_rotulos_lv1 = []
matriz_rotulos_lv2 = []
matriz_casa = []

matriz_apriori = []
with open('Saidas/AprioriAllBin.txt',  'rb') as fileBin:
    matriz_apriori = pickle.load(fileBin)
fileBin.close()

lerCSV("correlacao_sensores.csv", matriz_correlacao_sensores)
lerCSV("Saidas/classif_results_lv1.csv", matriz_rotulos_lv1)
lerCSV("Saidas/matrix_casa.csv", matriz_casa)

list_timestamps_apriori = []
for i in range(1,len(matriz_casa)):
    if(matriz_casa[i][1]) not in list_timestamps_apriori:
        list_timestamps_apriori.append(matriz_casa[i][1])

def filtro_correl_sensores_novo():
    mtx_aux = []
    data_inicio = '14-04-2019 00:00' #Hardcoded adaptado para a base
    data_fim = '27-05-2019 23:59' #Hardcoded adaptado para a base

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
    groups = [4]
    saida = []

    #j, k = 0, 0
    
    for group_correl in matriz_apriori:
        if group_correl:
            len_grupo = len(group_correl[0])
            
            if len_grupo in groups:

                for j in range(0,1):
                #for j in range(9, len(group_correl)):
                    
                    k = 0
                    #while k < (len_grupo-1):
                    count_timestamp = 0
                    idx_timestamp = 0
                    match = False

                    x = 1
                    while x < len(matriz_casa):
                        idx_timestamp = list_timestamps_apriori.index(matriz_casa[x][1])
                        increm_k = False

                        if x == 181:
                            print("")

                        if matriz_casa[x][0] == group_correl[j][k]:
                            count_timestamp = count_timestamp + 1

                            if x + count_timestamp < len(matriz_casa)-1:
                                while matriz_casa[x+count_timestamp][1] == list_timestamps_apriori[idx_timestamp] or matriz_casa[x+count_timestamp][1] == list_timestamps_apriori[idx_timestamp+1]:
                                    if matriz_casa[x+count_timestamp][0] == group_correl[j][k+1]:
                                        if k == len_grupo-2:
                                            match = True
                                            k = 0
                                            #count_timestamp = 0
                                            break
                                        else:
                                            k = k+1
                                            #count_timestamp = count_timestamp + 1
                                            x = x + count_timestamp
                                            count_timestamp = 0
                                            increm_k = True
                                            break
                                    else:
                                        count_timestamp = count_timestamp + 1
                                
                                if match:
                                    print("Grupo {} - LinhaApr: {} - Ultimo mtx_casa: {}".format(len_grupo, j, x+count_timestamp))
                                    saida.append([len_grupo, j, x+count_timestamp])
                                    match = False
                                elif k > 0 and not increm_k:
                                    k = 0
                                
                                
                                x = x + count_timestamp
                                count_timestamp = 0
                            else:
                                break
                        else:
                            x = x + 1
                        
                        #k = k+1

    return saida

def limpa_duplicatas_mtx2():
    for i in range(len(matriz_rotulos_lv2)):
        for j in range(i+1, len(matriz_rotulos_lv2)):
            if matriz_rotulos_lv2[i] == matriz_rotulos_lv2[j]:
                print("{} e {} repetidos".format(i,j))
                matriz_rotulos_lv2.pop(j)
                #limpa_duplicatas()

# Modo de correlação pelo arquivo de configuração (usuário)
matriz_rotulos_lv2 = filtro_correl_sensores_novo()

def sortIdx(val):
    return int(val[0])

matriz_rotulos_lv2.sort(key=sortIdx)

#limpa_duplicatas_mtx2()

with open('Saidas/classif_results_lv2.csv', 'w', newline='') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerow(['Id Home', 'Timestamp', 'Sensor Comodo', 'Comodo', 'Id Atividade', 'Atividade'])
    writer.writerows(matriz_rotulos_lv2)

writeFile.close()
'''

# Modo de correlação pelo AprioriAll gerado
saida_match_apriori = filtro_correl_sensores_aprioriall()
with open('Saidas/match_apriori.csv', 'w', newline='') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerow(['Grupo', 'Linha Apr', 'Último mtx_casa'])
    writer.writerows(saida_match_apriori)

writeFile.close()
'''
import csv
import time
from datetime import datetime as dt
from datetime import timedelta
import datetime
import segmentacao

#dados_casa: fornece a visão da base como um todo
#transições: tras a relação entre id_sensor (coluna) na base e IDs de timestamps onde ocorrem as transições
print("Segmentação em andamento")
indices_sensores = segmentacao.indices_sensores
dados_casa = segmentacao.dados_casa
dados_acesso = segmentacao.dados_acesso
transicoes = segmentacao.transicoes #Substituir esse e os outros por serialização
print("Segmentação finalizada")

#########################################
dict_categ_dia_atividades = {'1': "Dia útil", '2': "Fim de semana"}
dict_tipo_correl_sensores = {'1': "Presença", '2': "Luz/Aparelho"}
dict_transic_sensores = {}
dict_transic_rotulo = {}

def lerCSV(arquivo, matriz):
    leitura = open(arquivo, "r").readlines()
    for linha in leitura:
        matriz.append(linha.strip().split(','))

def filtro_periodo_dia(timestamp, id_periodo_dia, hora1, hora2, categ_dia):
    dt_aux = dt.strptime(timestamp[1:-1], '%Y-%m-%d %H:%M')

    #Testes para periodos definidos de atividades
    if hora1 != '' and dt_aux.time() < dt.strptime(hora1,'%H:%M').time():
        return False
    if hora2 != '' and dt_aux.time() > dt.strptime(hora2,'%H:%M').time():
        return False

    #Verificar se a restrição "dia útil/fim de semana" se aplica
    if (dt_aux.weekday() >= 0 and dt_aux.weekday() <= 4) and categ_dia != '1' and categ_dia != '0':
        return False
    if (dt_aux.weekday() == 5 or dt_aux.weekday() == 6) and categ_dia != '2' and categ_dia != '0':
        return False
    
    '''
    if id_periodo_dia == '1' and (dt_aux.time() >= dt.strptime("00:00",'%H:%M').time()) and (dt_aux.time() < dt.strptime("06:00",'%H:%M').time()):
        return True
    
    if id_periodo_dia == '2' and dt_aux.time() >= dt.strptime("06:00",'%H:%M').time() and dt_aux.time() < dt.strptime("12:00",'%H:%M').time():
        return True
    
    if id_periodo_dia == '3' and dt_aux.time() >= dt.strptime("12:00",'%H:%M').time() and dt_aux.time() < dt.strptime("18:00",'%H:%M').time():
        return True
    
    if id_periodo_dia == '4' and dt_aux.time() >= dt.strptime("18:00",'%H:%M').time() and dt_aux.time() <= dt.strptime("23:59",'%H:%M').time():
        return True
    '''
    
    #return False
    return True

def filtro_atv_comodo(id_atividade, id_sensor_comodo, valor_sensor):
    for i in range(1,len(matriz_atividades)):
        if id_atividade == matriz_atividades[i][0]:
            if matriz_atividades[i][6] == '0': return True

            for j in range(1,len(matriz_comodo_sensores)):
                if matriz_atividades[i][6] == matriz_comodo_sensores[j][0] and (str(id_sensor_comodo) == matriz_comodo_sensores[j][3] or str(id_sensor_comodo) == matriz_comodo_sensores[j][4] or str(id_sensor_comodo) == matriz_comodo_sensores[j][5]):
                    if matriz_atividades[i][7] == ''  or matriz_atividades[i][8] == '' or valor_sensor is None:
                        return True
                    elif matriz_atividades[i][7] == '1' and int(valor_sensor) <= int(matriz_atividades[i][8]):
                        return True
                    elif matriz_atividades[i][7] == '2' and int(valor_sensor) == int(matriz_atividades[i][8]):
                        return True
                        
    return False

indices_transicoes = []
matriz_comodo_sensores = []
matriz_atividades = []
matriz_correlacao_sensores = []

lerCSV("id_comodo_sensores.csv", matriz_comodo_sensores)
lerCSV("atividades.csv", matriz_atividades)
lerCSV("correlacao_sensores.csv", matriz_correlacao_sensores)

print("Iniciando classificação")

'''
for i in range(len(transicoes)):
    for j in range(1,len(transicoes[i])):
        if transicoes[i][j] not in indices_transicoes:
            indices_transicoes.append(transicoes[i][j])

indices_transicoes.sort()
indices_transicoes.remove(-1)
indices_transicoes.remove(1)
'''

for trc in transicoes:
    for i in range(1, len(matriz_comodo_sensores)):
        if (str(trc[0]) == matriz_comodo_sensores[i][3] or str(trc[0]) == matriz_comodo_sensores[i][4]):
            dict_transic_sensores[trc[0]] = matriz_comodo_sensores[i][1]
            break


test_periodo = False
test_atv_comodo = False
test_correlacao = False

matriz_rotulos_lv1 = []
matriz_rotulos_lv2 = []

for k in range(len(transicoes)):
    indice_sensor_comodo = transicoes[k][0]
    indices_transicoes = transicoes[k][1:len(transicoes[k])]

    for i in range(1,len(dados_casa)):
        if int(dados_casa[i][0]) in indices_transicoes: #Houve transição na linha da base analisada
            for j in range(1,len(matriz_atividades)): #Varrer lista de atividades registradas pra fazer match
                #Verifica se os requisitos descritos no arquivo de atividades são atendidos
                test_periodo = filtro_periodo_dia(dados_casa[i][1], matriz_atividades[j][2], matriz_atividades[j][3], matriz_atividades[j][4], matriz_atividades[j][5])
                
                #Se falhou no primeiro teste, pular para próxima iteração
                if not test_periodo: continue

                #Apenas considera sensores elegíveis para identificar transições (sensores de luz ou presença de acordo com o cômodo)
                if not indice_sensor_comodo in dict_transic_sensores.keys(): continue

                test_atv_comodo = filtro_atv_comodo(matriz_atividades[j][0], indice_sensor_comodo, dados_casa[i][indice_sensor_comodo])

                if test_atv_comodo:
                    #dict_transic_rotulo[dados_casa[i][0]] = matriz_atividades[j][1]
                    aux_classif = [dados_casa[i][0], dados_casa[i][1].replace('"',''), indice_sensor_comodo, dict_transic_sensores[indice_sensor_comodo], matriz_atividades[j][0], matriz_atividades[j][1]]
                    matriz_rotulos_lv1.append(aux_classif)
                else: continue
                
                #Verifica se os requisitos descritos no arquivo de correlação entre sensores são atendidos
                #test_correlacao = filtro_correl_sensores(i, matriz_atividades[j][0], indice_sensor_comodo)
                
                '''
                if test_correlacao:
                    #dict_transic_rotulo[dados_casa[i][0]] = matriz_atividades[j][1]
                    aux_classif = [dados_casa[i][0], dados_casa[i][1], indice_sensor_comodo, dict_transic_sensores[indice_sensor_comodo], matriz_atividades[j][1]]
                    matriz_rotulos_lv2.append(aux_classif)
                '''

def sortIdx(val):
    return int(val[0])

matriz_rotulos_lv1.sort(key=sortIdx)

with open('Saidas/classif_results_lv1.csv', 'w', newline='') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerow(['Id Home', 'Timestamp', 'Sensor Comodo', 'Comodo', 'Id Atividade', 'Atividade'])
    writer.writerows(matriz_rotulos_lv1)

writeFile.close()

'''
matriz_rotulos_lv2 = filtro_correl_sensores_novo()

with open('Saidas/classif_results_lv2.csv', 'w', newline='') as writeFile2:
    writer = csv.writer(writeFile2)
    writer.writerow(['Id Home', 'Timestamp', 'Sensor Comodo', 'Comodo', 'Rotulo'])
    writer.writerows(matriz_rotulos_lv2)
'''

print("Classificação finalizada")
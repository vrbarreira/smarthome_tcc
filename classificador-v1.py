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
transicoes = segmentacao.transicoes
print("Segmentação finalizada")

#########################################
dict_categ_dia_atividades = {'1': "Dia útil", '2': "Fim de semana"}
dict_tipo_correl_sensores = {'1': "Presença", '2': "Luz/Aparelho"}
dict_transic_rotulo = {}

def lerCSV(arquivo, matriz):
    leitura = open(arquivo, "r").readlines()
    for linha in leitura:
        matriz.append(linha.strip().split(';'))

def filtro_periodo_dia(timestamp, id_periodo_dia, hora1, hora2, categ_dia):
    dt_aux = dt.strptime(timestamp[1:-1], '%Y-%m-%d %H:%M')

    #Testes para periodos definidos de atividades
    if hora1 != '' and dt_aux.time() < dt.strptime(hora1,'%H:%M').time():
        return False
    if hora2 != '' and dt_aux.time() > dt.strptime(hora2,'%H:%M').time():
        return False

    #Verificar se a restrição "dia útil/fim de semana" se aplica
    if (dt_aux.weekday() >= 0 and dt_aux.weekday() <= 4) and categ_dia != '1':
        return False
    if (dt_aux.weekday() == 5 or dt_aux.weekday() == 6) and categ_dia != '2':
        return False
    
    if id_periodo_dia == '1' and (dt_aux.time() >= dt.strptime("00:00",'%H:%M').time()) and (dt_aux.time() < dt.strptime("06:00",'%H:%M').time()):
        return True
    
    if id_periodo_dia == '2' and dt_aux.time() >= dt.strptime("06:00",'%H:%M').time() and dt_aux.time() < dt.strptime("12:00",'%H:%M').time():
        return True
    
    if id_periodo_dia == '3' and dt_aux.time() >= dt.strptime("12:00",'%H:%M').time() and dt_aux.time() < dt.strptime("18:00",'%H:%M').time():
        return True
    
    if id_periodo_dia == '4' and dt_aux.time() >= dt.strptime("18:00",'%H:%M').time() and dt_aux.time() <= dt.strptime("23:59",'%H:%M').time():
        return True
    
    return False

def filtro_correl_sensores(id_linha_base, id_atividade):
    result = True
    
    for i in range(1,len(matriz_correlacao_sensores)):
        if matriz_correlacao_sensores[i][2] == id_atividade:
            id_sensor_1 = int(matriz_correlacao_sensores[i][0])
            id_sensor_2 = int(matriz_correlacao_sensores[i][1])
            tipo_1 = matriz_correlacao_sensores[i][3]
            tipo_2 = matriz_correlacao_sensores[i][4]
            valor_1 = int(matriz_correlacao_sensores[i][5])
            valor_2 = int(matriz_correlacao_sensores[i][6])

            teste_1 = (tipo_1 == '1' and int(dados_casa[id_linha_base][id_sensor_1]) <= valor_1) or (tipo_1 == '2' and int(dados_casa[id_linha_base][id_sensor_1]) == valor_1)    
            teste_2 = (tipo_2 == '1' and int(dados_casa[id_linha_base][id_sensor_2]) <= valor_2) or (tipo_2 == '2' and int(dados_casa[id_linha_base][id_sensor_2]) == valor_2)

            result = result and teste_1 and teste_2

            if not result: break

    return result

indices_transicoes = []
matriz_comodo_sensores = []
matriz_atividades = []
matriz_correlacao_sensores = []

lerCSV("id_comodo_sensores.csv", matriz_comodo_sensores)
lerCSV("atividades.csv", matriz_atividades)
lerCSV("correlacao_sensores.csv", matriz_correlacao_sensores)

print("Iniciando classificação")

for i in range(len(transicoes)):
    for j in range(1,len(transicoes[i])):
        if transicoes[i][j] not in indices_transicoes:
            indices_transicoes.append(transicoes[i][j])

indices_transicoes.sort()
indices_transicoes.remove(-1)
indices_transicoes.remove(1)

test_periodo = False
test_correlacao = False

for i in range(1,len(dados_casa)):
    if int(dados_casa[i][0]) in indices_transicoes: #Houve transição na linha da base analisada
        for j in range(1,len(matriz_atividades)): #Varrer lista de atividades registradas pra fazer match
            #Verifica se os requisitos descritos no arquivo de atividades são atendidos
            test_periodo = filtro_periodo_dia(
                dados_casa[i][1], matriz_atividades[j][2], matriz_atividades[j][3], matriz_atividades[j][4], matriz_atividades[j][5])
            
            #Se falhou no primeiro teste, pular para próxima iteração
            if not test_periodo: continue
            
            #Verifica se os requisitos descritos no arquivo de correlação entre sensores são atendidos
            test_correlacao = filtro_correl_sensores(i, matriz_atividades[j][0])

            if test_periodo and test_correlacao:
                dict_transic_rotulo[dados_casa[i][0]] = matriz_atividades[j][1]
            

print("Finalizado")
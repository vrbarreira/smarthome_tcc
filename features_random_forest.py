from datetime import datetime as dt
import csv
import pickle
import datetime

dias_da_semana = [
    'Segunda-feira',
    'Terça-feira',
    'Quarta-feira',
    'Quinta-Feira',
    'Sexta-feira',
    'Sábado',
    'Domingo'
]
dict_transicoes = {}
dados_casa = []
matriz_rotulos_lv2 = []

def lerCSV(arquivo, matriz):
    with open(arquivo, "r") as arq:
        leitura = arq.readlines()
        for linha in leitura:
            matriz.append(linha.strip().split(','))
    arq.close()

"""
entradas
vetor: vetor de vetores
vetor_col: vetor de indices
esta funcao diz quantas transicoes do tipo on/off existem para todos os aparelhos presentes na entrada da funcao e
mostra em forma de porcentagem o tempo que os aparelhos ficaram ligados. Retorna 2 vetores
onde a resposta desejada esta no indice vetor_col
"""
def feature_vector_aparelho(vetor, vetor_col):
	estado = []
	#vetor[0][2] = 0
	#vetor[0][27] = 1
	#vetor[7][2] = 0
	#vetor[8][27] = 1

	for i in range(len(vetor[0])):
		estado.append(vetor[0][i])
	transicao_on_off = [0]*len(vetor[0])
	tempo_ligado = [0]*len(vetor[0])

	for aparelho in vetor:
		for indice in vetor_col:
			if aparelho[indice] == '1':
				tempo_ligado[indice] += 1
			if aparelho[indice] != estado[indice]:
				transicao_on_off[indice] += 1 
				estado[indice] = aparelho[indice]

	for indice in vetor_col:
		tempo_ligado[indice] = tempo_ligado[indice]/len(vetor)

	return transicao_on_off, tempo_ligado

"""
entradas
vetor: vetor de dados
col: indice do vetor que contem a informacao de interesse
esta funcao diz em qual dia da semana a atividade esta sendo realizada, horario de inicio, periodo 
e se o dia eh fim de semana ou nao.
"""
def feature_tempo(vetor, col):
	global dias_da_semana
	
	ind_timestamp = col

	dia_data = dt.strptime(vetor[ind_timestamp][1:-1], '%Y-%m-%d %H:%M') 
	dia_semana = dias_da_semana[dia_data.weekday()]
	hora_inicio = datetime.time(dia_data.hour,dia_data.minute,)
	
	if hora_inicio.hour >= 0 and hora_inicio.hour <= 5:
		periodo = "madrugada"
	elif hora_inicio.hour >= 6 and hora_inicio.hour <= 11:
		periodo = "manha"
	elif hora_inicio.hour >= 12 and hora_inicio.hour <= 17:
		periodo = "tarde"
	elif hora_inicio.hour >= 18 and hora_inicio.hour <= 23:
		periodo = "noite"

	if dia_semana == "Domingo" or dia_semana == "Sábado":
		fim_semana = True
	else:
		fim_semana = False

	return hora_inicio, dia_semana, dia_data, periodo, fim_semana

lerCSV("home.csv", dados_casa)
lerCSV("Saidas/classif_results_lv2.csv", matriz_rotulos_lv2)

transicoes = []
with open('Saidas/indices_transic_bin.txt',  'rb') as fileBin:
    transicoes = pickle.load(fileBin)
fileBin.close()

for sensor in transicoes:
    sensor.pop()
    sensor.pop(1)

for i in range(len(dados_casa)):
    if i > 0: dict_transicoes[dados_casa[i][0]] = i

def add_features():
    vetor = []
    matriz_comodo_sensores = []
    vec_on_off, vec_tempo_ligado = [],[]
    mtx_features = []

    lerCSV("id_comodo_sensores.csv", matriz_comodo_sensores)
    
    for i in range(1,len(matriz_rotulos_lv2)):
        for j in range(len(transicoes)):
            if transicoes[j][0] == int(matriz_rotulos_lv2[i][2]):
                tipo = 0
                sensor_luz, sensor_presenca, sensor_aparelho = 0,0,0
                lig_desl_luz, lig_desl_presenca, lig_desl_aparelho = 0,0,0
                tempo_lig_luz, tempo_lig_presenca, tempo_lig_aparelho = 0,0,0

                for k in range(1,len(matriz_comodo_sensores)):
                    if str(transicoes[j][0]) == matriz_comodo_sensores[k][3] and matriz_comodo_sensores[k][2] == '1':
                        tipo = int(matriz_comodo_sensores[k][2])
                        sensor_luz = int(matriz_comodo_sensores[k][3])
                        break
                    elif str(transicoes[j][0]) == matriz_comodo_sensores[k][4] and matriz_comodo_sensores[k][2] == '2':
                        tipo = int(matriz_comodo_sensores[k][2])
                        sensor_luz = int(matriz_comodo_sensores[k][3])
                        sensor_presenca = int(matriz_comodo_sensores[k][4])
                        break
                    elif str(transicoes[j][0]) == matriz_comodo_sensores[k][4] and matriz_comodo_sensores[k][2] == '3':
                        tipo = int(matriz_comodo_sensores[k][2])
                        sensor_luz = int(matriz_comodo_sensores[k][3])
                        sensor_presenca = int(matriz_comodo_sensores[k][4])
                        sensor_aparelho = int(matriz_comodo_sensores[k][5])
                        break
                
                if (sensor_luz == 0 and sensor_presenca == 0 and sensor_aparelho == 0) or tipo == 0:
                    print("ERRO!")
                    return

                for k in range(1, len(transicoes[j])-1):
                    if transicoes[j][k] == int(matriz_rotulos_lv2[i][0]):                       
                        idx_vec_inicio = dict_transicoes[str(transicoes[j][k])]
                        idx_vec_fim = dict_transicoes[str(transicoes[j][k+1])]

                        #if idx_vec_fim == len(dados_casa): idx_vec_fim = idx_vec_fim - 1
                        
                        vetor = dados_casa[idx_vec_inicio:idx_vec_fim]
                        
                        hora_inicio, dia_semana, dia_data, periodo, fim_semana = feature_tempo(vetor[0], 1)

                        if tipo == 1:
                            vec_on_off, vec_tempo_ligado = feature_vector_aparelho(vetor,[sensor_luz])
                            lig_desl_luz = vec_on_off[sensor_luz]
                            tempo_lig_luz = vec_tempo_ligado[sensor_luz]
                        elif tipo == 2:
                            vec_on_off, vec_tempo_ligado = feature_vector_aparelho(vetor,[sensor_luz,sensor_presenca])
                            lig_desl_luz, lig_desl_presenca = vec_on_off[sensor_luz], vec_on_off[sensor_presenca]
                            tempo_lig_luz, tempo_lig_presenca = vec_tempo_ligado[sensor_luz], vec_tempo_ligado[sensor_presenca]
                        elif tipo == 3:
                            vec_on_off, vec_tempo_ligado = feature_vector_aparelho(vetor,[sensor_luz,sensor_presenca,sensor_aparelho])
                            lig_desl_luz, lig_desl_presenca, lig_desl_aparelho = vec_on_off[sensor_luz], vec_on_off[sensor_presenca], vec_on_off[sensor_aparelho]
                            tempo_lig_luz, tempo_lig_presenca, tempo_lig_aparelho = vec_tempo_ligado[sensor_luz], vec_tempo_ligado[sensor_presenca], vec_tempo_ligado[sensor_aparelho]
                        
                        mtx_features.append(matriz_rotulos_lv2[i][:2] + [str(hora_inicio.hour), str(hora_inicio.minute), periodo, str(fim_semana)] + matriz_rotulos_lv2[i][2:4] + 
                            [lig_desl_luz,lig_desl_aparelho,tempo_lig_luz,tempo_lig_aparelho] + matriz_rotulos_lv2[i][4:])
    
    return mtx_features

def vetor_indices(transic_inicio, transic_fim):
    vec_aux = []
    
    iniciar = False
    finalizar = False
    for i in range(1,len(dados_casa)):
        if dados_casa[i][0] == transic_inicio:
            iniciar = True
        elif dados_casa[i][0] == transic_fim:
            finalizar = True
        
        if iniciar:
            vec_aux.append(dados_casa[i])
        if finalizar:
            break

    return vec_aux

mtx_classif_features = add_features()

with open('Saidas/features_random_forest.csv', 'w', newline='') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerow(['Id Home', 'Timestamp', 'Hora', 'Minuto', 'Periodo', 'Fim de Semana','Sensor Comodo', 'Comodo', 
        'lig_desl_luz','lig_desl_aparelho','tempo_lig_luz','tempo_lig_aparelho','Id Atividade', 'Atividade'])
    writer.writerows(mtx_classif_features)
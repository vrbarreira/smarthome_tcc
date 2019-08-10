from scipy.stats import norm
from scipy.stats import binom
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
import time
from datetime import datetime as dt
from datetime import timedelta
import datetime

############################### funcoes de ajuda deletar dps ##############################

"""
printa as linhas da matrix de dados onde ocorre trancao de estado 1-0 ou 0-1 junto com os indices 
linhas: linhas da matrix 
indice: indice da linha onde ocorreu a transicao 
"""
def imprimeTransicoes(matrix_dados, vetor_col):
	estado = matrix_dados[0]
	indice = [[0]]*len(matrix_dados[0])
	linhas = [[0]]*len(matrix_dados[0])
	entra = True
	for i in range(len(matrix_dados)):
		for j in vetor_col:
			if entra and matrix_dados[i][j] != estado[j]:
				print(i,"dasdas")
				estado[j] = matrix_dados[i][j]
				indice[j]= [i]
				linhas[j]= [matrix_dados[i-1]]
				linhas[j].append(matrix_dados[i])
				linhas[j].append(matrix_dados[i+1]) 

				entra = False
			
			elif matrix_dados[i][j] != estado[j]:
				estado[j] = matrix_dados[i][j]
				indice[j].append(i)
				linhas[j].append(matrix_dados[i-1])
				linhas[j].append(matrix_dados[i])
				linhas[j].append(matrix_dados[i+1]) 
	return linhas, indice
"""
testa os segmentos das transicoes 
"""
def testa_trasicao(matrix_dados, transicoes, size_janela):
	escada = transicoes[0]
	aquario = transicoes[1]
	banho = transicoes[2]
	
	funciona = True
	i=1
	#while i < len(escada)-1:
	for i in range(1,len(escada)-1):
		indice_inicial = escada[i]
		k = indice_inicial +1 
		estado = matrix_dados[indice_inicial][5]
		#if estado == 1: 
		indice_final = escada[i+1]
		while k < indice_final:
			if estado != matrix_dados[k][5] and estado != matrix_dados[k+1][5] and estado != matrix_dados[k+2][5]:
				print("multiplos estados no segmento na escada")
				print("indice inicial: ", indice_inicial)
				print("indie final: ", indice_final)
				funciona = False
				break
			k += 1
			#i += 2
		#else:
		#	i += 1
		if not(funciona):
			break
	if funciona:
		print("escada ok")
	funciona = True
	for i in range(1,len(aquario)-1):
		indice_inicial = aquario[i]
		k = indice_inicial +1 
		estado = matrix_dados[indice_inicial][10]
		#if estado == 1: 
		indice_final = aquario[i+1]
		while k < indice_final:
			if estado != matrix_dados[k][10] and estado != matrix_dados[k+1][10] and estado != matrix_dados[k+2][10]:
				print("multiplos estados no segmento no aquario")
				print("indice inicial: ", indice_inicial)
				print("indie final: ", indice_final)
				funciona = False
				break
			k += 1
			#i += 2
		#else:
		#	i += 1
		if not(funciona):
			break
	if funciona:
		print("aquario ok")
	funciona = True
	for i in range(1,len(banho)-1):
		indice_inicial = banho[i]
		k = indice_inicial +1 
		estado = matrix_dados[indice_inicial][13]
		#if estado == 1: 
		indice_final = banho[i+1]
		while k < indice_final:
			if estado != matrix_dados[k][13] and estado != matrix_dados[k+1][13] and estado != matrix_dados[k+2][13] and estado != matrix_dados[k+3][13]:
				print("multiplos estados no segmento no banho")
				print("indice inicial: ", indice_inicial)
				print("indie final: ", indice_final)
				funciona = False
				break
			k += 1
			#i += 2
		#else:
		#	i += 1
		if not(funciona):
			break
	if funciona:
		print("banho ok")
	
	funciona = True
	for elemento in transicoes[3:]:
		indice_col = elemento[0]
		for i in range(len(elemento)-1):
			indice_inicial = elemento[i]
			k = indice_inicial
			indice_final = elemento[i+1]
			if matrix_dados[indice_inicial][indice_col] < 150:
				presente = True
			else:
				presente = False
			while k < indice_final:
				if presente:
					if matrix_dados[k][indice_col] >= 150:
						print("pessoa esta ausente no segmento")
						print("sensor: ", matrix_dados[0][indice_col])
						print("indice inicial: ", indice_inicial)
						print("indice final: ", indice_final)
						funciona = False
						break

				else:
					if matrix_dados[k][indice_col] < 150:
						print("pessoa esta presente no segmento")
						print("sensor: ", matrix_dados[0][indice_col])
						print("indice inicial: ", indice_inicial)
						print("indice final: ", indice_final)
						funciona = False
						break
				k+=1
			if not(funciona):
				break
		if funciona:
			print(print("segmentos ok: ", matrix_dados[0][indice_col]))
		funciona = True
			

					

############################### dados da casa #################################
id_luz_sala = 2
id_pres_sala = 15
id_tv_sala = 27

id_luz_cozinha = 3
id_luz_dispensa = 7
id_pres_cozinha = 16
id_tv_cozinha = 25

id_luz_lavanderia = 4
id_pres_lavanderia = 17
id_som_lavanderia = 29

id_luz_escada = 5

id_luz_garagem = 6
id_pres_garagem = 18

id_luz_cobertura = 11
id_pres_cobertura = 21

id_luz_corredor = 12
id_pres_corredor = 22

id_luz_quarto1 = 8
id_pres_quarto1 = 19
id_vent_quarto1 = 24

id_luz_quarto2 = 9
id_pres_quarto2 = 20
id_vent_quarto2 = 25

id_luz_quarto3 = 14
id_pres_quarto3 = 23
id_vent_quarto3 = 26

id_luz_banheiro = 13

id_luz_aquario = 10

#Índices do log de entrada por cômodo (hardcoded, será customizável em versão futura)
sala = [id_luz_sala,id_pres_sala,id_tv_sala]
cozinha = [id_luz_cozinha,id_luz_dispensa,id_pres_cozinha,id_tv_cozinha]
lavanderia = [4,17,29] #luz, presença, som
escada = [5] #luz
garagem = [6,18] #luz, presença
cobertura = [11,21] #luz, presença
corredor = [12,22] #luz, presença
quarto1 = [8,19,24] #luz, presença, ventilador
quarto2 = [9,20,25] #luz, presença, ventilador
quarto3 = [14,23,26] #luz, presença, ventilador
banheiro = [13] #luz
aquario = [10] #luz

casa = [sala, cozinha, lavanderia, escada, garagem, cobertura, corredor, quarto1, quarto2, quarto3, banheiro, aquario]

############################### dados da casa #################################
dados_casa = [] #Arquivo de entrada contendo os dados de sensores da casa
transicoes = [] #Índices de mudança de estado de todos os sensores
dias_casa = [] #Índice no qual um dia acaba

############################### dados de acesso na casa #################################
dados_acesso = [] #Arquivo de entrada contendo os dados de acessos da casa
dias_acesso = [] #Índice no qual um dia acaba


#Índices hardcode. Esta parte será customizável em versão futura
#luz_escada, luz_aquario, luz_banho, pres_sala, pres_cozinha pres_lavanderia, pres_garagem, pres_quarto1, pres_quarto2, pres_quarto3
indices_sensores = [5,10,13,15, 16, 17, 18, 19, 20, 21, 22, 23]
#Foram escolhidos sensores de presença ou de luz, quando não há sensor de presença no cômodo

dias_da_semana = [
    'Segunda-feira',
    'Terça-feira',
    'Quarta-feira',
    'Quinta-Feira',
    'Sexta-feira',
    'Sábado',
    'Domingo'
]

# Extração de dados dos sensores da casa
def init_dados_casa():
	global dados_casa
	global transicoes
	global dias_casa
	global indices_sensores

	#Obs: sempre se atentar ao modelo de dados fornecido (quais colunas são fornecidas)
	arquivo = open("home.csv", "r") #leitura inicial do arquivo

	#Tratamento do cabeçalho
	line = arquivo.readline()
	lineSplit = line.split(",") #separa os campos do cabeçalho num vetor
	lineSplit[-1] = lineSplit[-1][:-1]
	dados_casa.append(lineSplit)

	#Tratamento dos dados de sensores
	for line in arquivo:
		lineSplit = line.split(",")
		lineSplit[2:] =  list(map(int,lineSplit[2:])) #Conversão das leituras de sensores para int
		dados_casa.append(lineSplit)
	arquivo.close()
	#Identificação de transições (escada, aquario, banho, presença)
	size_janela = 3
	add_transicao = True
	for j in indices_sensores: 
		transicao_col = [j]
		acesa = dados_casa[1][j] #indica se a luz esta acesa ou nao
		if j > 14:
			add_transicao = False
			if dados_casa[1][j] < 50:
				presente = True
			else:
				presente = False
		
		for i in range(1, len(dados_casa) - size_janela): 
			if j > 14: #Presenças
				hora_casa_atual = dt.strptime(dados_casa[i][1][1:-1], '%Y-%m-%d %H:%M')
				hora_casa_seguinte = dt.strptime(dados_casa[i][1][1:-1], '%Y-%m-%d %H:%M')
				dif_pres = timedelta(seconds = dados_casa[i+1][j] - dados_casa[i][j]) #tempo que foi incrementado no sensor de presenca 
				#for k in range(1,size_janela+1):
					#if dados_casa[i][j] <= dados_casa[i+k][j]:  
						#add_transicao = False
						#break
				"""
				if j == 16:
					a = dados_casa[i][j]
					b = dados_casa[i+1][j]
					c = dados_casa[i][0]
				"""
				if (dados_casa[i][j] > dados_casa[i+1][j] or (hora_casa_seguinte - hora_casa_atual)/2 > dif_pres) and dados_casa[i+1][j] < 150 and not(presente):
					presente = True
					add_transicao = True
				elif (presente and dados_casa[i+1][j] >= 150) or hora_casa_seguinte - hora_casa_atual > timedelta(minutes = 30):
					presente = False
					add_transicao = True
				
				
			else: #luz_escada, luz_aquario, luz_banho (Cômodos s/ sensor de presença)
				for k in range(1,size_janela+1):
					"""
					a = dados_casa[i-(size_janela + 1)][j]
					b = dados_casa[i][j] 
					c = dados_casa[i+1][j]
					d = dados_casa[i-1]
					e = dados_casa[i]
					f = dados_casa[i+1]
					g = i-(size_janela) + 1
					"""
					
					if dados_casa[i][j] == dados_casa[i+k][j]:
						add_transicao = False
						break
					elif dados_casa[i][j]!= dados_casa[i-1][j] and dados_casa[i][j] != dados_casa[i+1][j]: #teste para ver se é um elemento isolado
						for l in range(1,size_janela +1):
							if acesa:
								if dados_casa[i+l][j] == 1:
									add_transicao =False
									break
							else:
								if dados_casa[i+l][j] == 0:
									add_transicao = False
									break
								
						if not(add_transicao):
							break
			if add_transicao:
				if j<= 14:
					if dados_casa[i+1][j] == 1:
						acesa = True
					else:
						acesa = False
				transicao_col.append(i+1)

			if j <= 14:
				add_transicao = True
			else:
				add_transicao = False
		transicao_col.insert(1,1)
		transicao_col.append(-1)
		transicoes.append(transicao_col)
	

	for i in range(1,len(dados_casa)-1):
		datetime_dia = dt.strptime(dados_casa[i][1][1:11], '%Y-%m-%d')
		datetime_prox_dia = dt.strptime(dados_casa[i+1][1][1:11], '%Y-%m-%d')
		if datetime_prox_dia > datetime_dia:
			dias_casa.append(i+1)


	dias_casa.append(-1)
	#print(dias_casa)
	#print(transicoes)

	"""
	for i in range(len(dias_casa)-1):
		inicio = dias_casa[i]
		fim = dias_casa[i+1]
		print(dados_casa[fim-1])
		print(dados_casa[fim])
		print(dados_casa[fim+1],fim)
		print("\n\n")
	"""

# Extração de dados do portão de acesso
def init_dados_acesso():
	global dados_acesso
	global dias_acesso # cada dois indices seguidos corresponde a um dia
	arquivo = open("access.csv", "r")
	line = arquivo.readline()
	lineSplit = line.split(",")
	dados_acesso.append(lineSplit)

	for line in arquivo:
		lineSplit = line.split(",")
		lineSplit[1] =  time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime(int(lineSplit[1]))) #Timestamp UNIX p/ datetime
		dados_acesso.append(lineSplit)
	arquivo.close()
	i = 1
	dias_acesso.append(1)
	while i < len(dados_acesso)-1:
		dia_atual = dt.strptime(dados_acesso[i][1], '%Y/%m/%d, %H:%M:%S')
		dia_seguinte = dt.strptime(dados_acesso[i+1][1], '%Y/%m/%d, %H:%M:%S')
		if dia_seguinte.date() > dia_atual.date():
			dias_acesso.append(i+1)
		if dia_atual >= dia_seguinte:
			del dados_acesso[i+1]
		else:
			i += 1
		
	
	"""
	funciona
	for i in range(1,len(dados_acesso)-1):
		datetime_dia = dt.strptime(dados_acesso[i][1][:10], '%Y/%m/%d')
		datetime_prox_dia = dt.strptime(dados_acesso[i+1][1][:10], '%Y/%m/%d')
		if datetime_prox_dia > datetime_dia:
			dias_acesso.append(i+1)
	"""
	dias_acesso.append(-1)# referencia para o ultimo indice da matrix dados_acesso

	#escada_linha, escada_indie = imprimeTransicoes(dados_casa[1:], [5]) 
	#print(dias_acesso)

init_dados_casa()
init_dados_acesso()

################### Extracao das features para classificacao #######################
indice = transicoes[3][2]
vetor = dados_casa[4:indice] 

#print(vetor)

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
	vetor[0][2] = 0
	vetor[0][27] = 1
	vetor[7][2] = 0
	vetor[8][27] = 1

	for i in range(len(vetor[0])):
		estado.append(vetor[0][i])
	transicao_on_off = [0]*len(vetor[0])
	tempo_ligado = [0]*len(vetor[0])

	for aparelho in vetor:
		for indice in vetor_col:
			if aparelho[indice] == 1:
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
	
	ind_timestamp = col[0]

	dia_data = dt.strptime(vetor[ind_timestamp][1:-1], '%Y-%m-%d %H:%M') 
	dia_semana = dias_da_semana[dia_data.weekday()]
	hora_inicio = datetime.time(dia_data.hour,dia_data.minute,)
	
	if hora_inicio.hour >= 0 and hora_inicio.hour <= 4:
		periodo = "madrugada"
	elif hora_inicio.hour >= 5 and hora_inicio.hour <= 11:
		periodo = "manha"
	elif hora_inicio.hour >= 12 and hora_inicio.hour <= 18:
		periodo = "tarde"
	elif hora_inicio.hour >= 19 and hora_inicio.hour <= 23:
		periodo = "noite"

	if dia_semana == "Domingo" or dia_semana == "Sábado":
		fim_semana = True
	else:
		fim_semana = False

	return hora_inicio, dia_semana, dia_data, periodo, fim_semana

############################### funcoes de ajuda deletar dps ##############################

#Teste de verificação com dados da casa
print(dados_casa[0][2],dados_casa[0][15],dados_casa[0][27])
#print(vetor)
#print(feature_vector_aparelho(vetor,[2,27]))
print(dados_casa[0][1],dados_casa[0][15])
#print(feature_tempo(vetor[0],[1,15]))
testa_trasicao(dados_casa,transicoes,3)



#for i in range(len(dias_acesso)-1):
#	inicio = dias_acesso[i]
#	fim = dias_acesso[i+1]
#	print(dados_acesso[inicio:fim])
#	print("\n\n")


"""
printa as linhas da matrix de dados onde ocorre trancao de estado 1-0 ou 0-1 junto com os indices 
linhas: linhas da matrix 
indice: indice da linha onde ocorreu a transicao 
"""
def imprimeTransicoes(matrix_dados, vetor_col):
	estado = matrix_dados[0]
	indice = [[0]]*len(matrix_dados[0])
	linhas = [[0]]*len(matrix_dados[0])
	entra = True
	for i in range(len(matrix_dados)):
		for j in vetor_col:
			if entra and matrix_dados[i][j] != estado[j]:
				print(i,"dasdas")
				estado[j] = matrix_dados[i][j]
				indice[j]= [i]
				linhas[j]= [matrix_dados[i-1]]
				linhas[j].append(matrix_dados[i])
				linhas[j].append(matrix_dados[i+1]) 

				entra = False
			
			elif matrix_dados[i][j] != estado[j]:
				estado[j] = matrix_dados[i][j]
				indice[j].append(i)
				linhas[j].append(matrix_dados[i-1])
				linhas[j].append(matrix_dados[i])
				linhas[j].append(matrix_dados[i+1]) 
	return linhas, indice

"""
testa os segmentos das transicoes 
"""
def testa_transicao(matrix_dados, transicoes):
	for elemento in transicoes:
		elemento.insert(1,1)
		elemento.append(-1)
	escada = transicoes[0]
	aquario = transicoes[1]
	banho = transicoes[2]
	
	funciona = True
	i=1
	#while i < len(escada)-1:
	for i in range(1,len(escada)-1):
		indice_inicial = escada[i]
		k = indice_inicial +1 
		estado = matrix_dados[indice_inicial][5]
		#if estado == 1: 
		indice_final = escada[i+1]
		while k < indice_final:
			if estado != matrix_dados[k][5] and estado != matrix_dados[k+1][5] and estado != matrix_dados[k+2][5] and estado != matrix_dados[k+3][5]:
				print("multiplos estados no segmento na escada")
				print("indice inicial: ", indice_inicial)
				print("indice final: ", indice_final)
				funciona = False
				break
			k += 1
			#i += 2
		#else:
		#	i += 1
		if not(funciona):
			break
	if funciona:
		print("escada ok")
	funciona = True
	for i in range(1,len(aquario)-1):
		indice_inicial = aquario[i]
		k = indice_inicial +1 
		estado = matrix_dados[indice_inicial][10]
		#if estado == 1: 
		indice_final = aquario[i+1]
		while k < indice_final:
			if estado != matrix_dados[k][10] and estado != matrix_dados[k+1][10] and estado != matrix_dados[k+2][10] and estado != matrix_dados[k+3][10]:
				print("multiplos estados no segmento no aquario")
				print("indice inicial: ", indice_inicial)
				print("indie final: ", indice_final)
				funciona = False
				break
			k += 1
			#i += 2
		#else:
		#	i += 1
		if not(funciona):
			break
	if funciona:
		print("aquario ok")
	funciona = True
	for i in range(1,len(banho)-1):
		indice_inicial = banho[i]
		k = indice_inicial +1 
		estado = matrix_dados[indice_inicial][13]
		#if estado == 1: 
		indice_final = banho[i+1]
		while k < indice_final:
			if estado != matrix_dados[k][13] and estado != matrix_dados[k+1][13] and estado != matrix_dados[k+2][13] and estado != matrix_dados[k+3][13]:
				print("multiplos estados no segmento no banho")
				print("indice inicial: ", indice_inicial)
				print("indie final: ", indice_final)
				funciona = False
				break
			k += 1
			#i += 2
		#else:
		#	i += 1
		if not(funciona):
			break
	if funciona:
		print("banho ok")
	
	funciona = True
	for elemento in transicoes[3:]:
		indice_col = elemento[0]
		for i in range(len(elemento)-1):
			indice_inicial = elemento[i]
			k = indice_inicial
			indice_final = elemento[i+1]
			if matrix_dados[indice_inicial][indice_col] < 150:
				presente = True
			else:
				presente = False
			while k < indice_final:
				if presente:
					if matrix_dados[k][indice_col] >= 150:
						print("pessoa esta ausente no segmento")
						print("sensor: ", matrix_dados[0][indice_col])
						print("indice inicial: ", indice_inicial)
						print("indice final: ", indice_final)
						funciona = False
						break

				else:
					if matrix_dados[k][indice_col] < 150:
						print("pessoa esta presente no segmento")
						print("sensor: ", matrix_dados[0][indice_col])
						print("indice inicial: ", indice_inicial)
						print("indice final: ", indice_final)
						funciona = False
						break
				k+=1
			if not(funciona):
				break
		if funciona:
			print(print("segmentos ok: ", matrix_dados[0][indice_col]))
		funciona = True


#Teste de verificação com dados da casa
#print(dados_casa[0][2],dados_casa[0][15],dados_casa[0][27])
#print(vetor)
#print(feature_vector_aparelho(vetor,[2,27]))

print(dados_casa[0][1],dados_casa[0][15])
#print(feature_tempo(vetor[0],[1,15]))
testa_transicao(dados_casa,transicoes)


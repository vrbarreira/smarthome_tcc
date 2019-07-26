from scipy.stats import norm
from scipy.stats import binom
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
import time
from datetime import datetime as dt
import datetime

id_luz_sala = 2
id_pres_sala = 15
id_tv_sala = 27
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




############################### dados da casa #################################

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
dados_casa = [] #Arquivo de entrada contendo os dados da casa
transicoes = [] #Índices de mudança de estado de todos os sensores da presença
dias_casa = [] #Índice no qual um dia acaba

############################### dados de acesso na casa #################################
dados_acesso = []
dias_acesso = [] #Índice no qual um dia acaba

#Índices hardcode. Esta parte será customizável em versão futura
#luz_escada, luz_aquario, luz_banho, pres_sala, pres_cozinha pres_lavanderia, pres_garagem, pres_quarto1, pres_quarto2, pres_quarto3
indices_sensores = [5,10,13,15, 16, 17, 18, 19, 20, 21, 22, 23]
#Foram escolhidos sensores de presença ou de luz, quando não há sensor de presença no cômodo
arquivo = open("access.csv", "r")
line = arquivo.readline()
lineSplit = line.split(",")
dados_acesso.append(lineSplit)

for line in arquivo:
    lineSplit = line.split(",")
    lineSplit[1] =  time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime(int(lineSplit[1]))) #Timestamp UNIX p/ datetime
    dados_acesso.append(lineSplit)
arquivo.close()

for i in range(1,len(dados_acesso)-1):
	datetime_dia = dt.strptime(dados_acesso[i][1][:10], '%Y/%m/%d')
	datetime_prox_dia = dt.strptime(dados_acesso[i+1][1][:10], '%Y/%m/%d')
	if datetime_prox_dia > datetime_dia:
		dias_acesso.append(i+1)
dias_acesso.append(-1)
escada_linha, escada_indie = imprimeTransicoes(dados_casa[1:], [5])
#print(dias_acesso)

################### Extracao das features para classificacao #######################
indice = transicoes[3][2]
vetor = dados_casa[4:indice] 

dias_da_semana = [
    'Segunda-feira',
    'Terça-feira',
    'Quarta-feira',
    'Quinta-Feira',
    'Sexta-feira',
    'Sábado',
    'Domingo'
]

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
		for i in range(1, len(dados_casa) - size_janela): 
			if j > 14: #Presenças
				for k in range(1,size_janela+1):
					if dados_casa[i][j] <= dados_casa[i+k][j]:
						add_transicao = False
						break

			else: #luz_escada, luz_aquario, luz_banho (Cômodos s/ sensor de presença)
				for k in range(1,size_janela+1):
					if dados_casa[i][j] == dados_casa[i+k][j]:
						add_transicao = False
						break
				
			if add_transicao:
				transicao_col.append(i+1)
			add_transicao = True

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
def init_dados_acesso():
	global dados_acesso
	global dias_acesso

	arquivo = open("access.csv", "r")
	line = arquivo.readline()
	lineSplit = line.split(",")
	dados_acesso.append(lineSplit)

	for line in arquivo:
		lineSplit = line.split(",")
		lineSplit[1] =  time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime(int(lineSplit[1]))) #Timestamp UNIX p/ datetime
		dados_acesso.append(lineSplit)
	arquivo.close()

	for i in range(1,len(dados_acesso)-1):
		datetime_dia = dt.strptime(dados_acesso[i][1][:10], '%Y/%m/%d')
		datetime_prox_dia = dt.strptime(dados_acesso[i+1][1][:10], '%Y/%m/%d')
		if datetime_prox_dia > datetime_dia:
			dias_acesso.append(i+1)
	dias_acesso.append(-1)
	#print(dias_acesso)

init_dados_casa()
init_dados_acesso()

################### Extracao das features para classificacao #######################
indice = transicoes[3][2]
vetor = dados_casa[4:indice] 

#Teste de verificação com dados da casa
print(dados_casa[0][2],dados_casa[0][15],dados_casa[0][27])
#print(vetor)

"""

entradas
vetor: vetor de vetores
vetor_col: vetor de indices

esta funcao diz quantas transicoes do tipo on/off existem para todos os aparelhos presentes na entrada da funcao e
mostra em forma de porcentagem o tempo que os aparelhos ficaram ligados
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

print(feature_vector_aparelho(vetor,[2,27]))

"""
entradas
vetor: vetor de dados
col: indice do vetor que contem a informacao de interesse

esta funcao diz em qual dia da semana a atividade esta sendo realizada, horario de inicio, periodo e se o dia eh fim de semana ou nao 
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



print(vetor)
print(dados_casa[0][1],dados_casa[0][15])
print(feature_tempo(vetor[0],[1,15]))

#for i in range(len(dias_acesso)-1):
#	inicio = dias_acesso[i]
#	fim = dias_acesso[i+1]
#	print(dados_acesso[inicio:fim])
#	print("\n\n")


"""
for i in range(1,lend(dados)): #range(1,len(dados)):
  luz_sala.append(int(dados[i][2]))
  if i+1 < len(dados):
    if int(dados[i][2]) != int(dados[i+1][2]):
      troca.append(i)

print(luz_sala,"dasdas")
print(troca)
plt.plot(range(len(luz_sala)),binom.pmf(luz_sala, len(luz_sala),0.99))
plt.show()
"""


"""
for i in range(1,60): #range(1,len(dados)):
  pres_sala.append(int(dados[i][15]))
  if i+1 < len(dados):
    if int(dados[i][15]) > int(dados[i+1][15]):
      print(dados[i][15], dados[i+1][15], i)
      troca.append(i)
  
print(pres_sala)
print(troca)
window = [pres_sala[i:i+5] for i in range(0, len(pres_sala), 5)]
print(window)
i = 0
j = 0 
print(window[0][0:1])
while i<len(window):
	plt.figure(1)
	plt.subplot(221)
	plt.plot(range(len(window[i][0:2])),norm.pdf(window[i][0:2]))
	plt.subplot(222)
	plt.plot(range(len(window[i][0:3])),norm.pdf(window[i][0:3]))
	plt.subplot(223)
	plt.plot(range(len(window[i][0:4])),norm.pdf(window[i][0:4]))
	plt.subplot(224)
	plt.plot(range(len(window[i][0:5])),norm.pdf(window[i][0:5]))
	print(window[i],"window")
	plt.show()
	sair = raw_input("continuar?")
	if sair != "s":
		break
	i+= 1
"""

""""

plt.figure(1)
plt.subplot(221)
plt.plot(range(len(pres_sala[troca[i]:troca[i+1]])),norm.pdf(pres_sala[troca[i]:troca[i+1]]))
plt.subplot(222)
plt.plot(range(len(pres_sala[troca[i]:troca[i+2]])),norm.pdf(pres_sala[troca[i]:troca[i+2]]))
plt.subplot(223)
plt.plot(range(len(pres_sala[troca[i]:troca[i+3]])),norm.pdf(pres_sala[troca[i]:troca[i+3]]))
plt.subplot(224)
plt.plot(range(len(pres_sala[troca[i]:troca[i+4]])),norm.pdf(pres_sala[troca[i]:troca[i+4]]))

plt.figure(1)
	plt.subplot(221)
	plt.plot(range(len(window[i][0:1])),norm.pdf(window[[i][0:1]]))
	plt.subplot(222)
	plt.plot(range(len(window[i][0:2])),norm.pdf(window[[i][0:2]]))
	plt.subplot(223)
	plt.plot(range(len(window[i][0:3])),norm.pdf(window[[i][0:3]]))
	plt.subplot(224)
	plt.plot(range(len(window[i][0:4])),norm.pdf(window[[i][0:4]]))
"""
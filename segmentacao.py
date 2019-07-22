from scipy.stats import norm
from scipy.stats import binom
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
import time
from datetime import datetime

############################### dados da casa #################################

dados_casa = [] #Arquivo de entrada contendo os dados da casa
transicoes = [] #Índices de mudança de estado de todos os sensores da presença
dias_casa = [] #Índice no qual um dia acaba

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

for j in [5,10,13,15, 16, 17, 18, 19, 20, 21, 22, 23]: 
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
			
			#if (dados_casa[i][j] != dados_casa[i+1][j]) and (dados_casa[i][j] != dados_casa[i+2][j]) and (dados_casa[i][j] != dados_casa[i+3][j]):
			#	transicao_col.append(i+1)
			
		if add_transicao:
			transicao_col.append(i+1)
		add_transicao = True

	transicoes.append(transicao_col)

for i in range(1,len(dados_casa)-1):
	datetime_dia = datetime.strptime(dados_casa[i][1][1:11], '%Y-%m-%d')
	datetime_prox_dia = datetime.strptime(dados_casa[i+1][1][1:11], '%Y-%m-%d')
	if datetime_prox_dia > datetime_dia:
		dias_casa.append(i+1)


dias_casa.append(-1)
print(dias_casa)
print(transicoes)

"""
for i in range(len(dias_casa)-1):
	inicio = dias_casa[i]
	fim = dias_casa[i+1]
	print(dados_casa[fim-1])
	print(dados_casa[fim])
	print(dados_casa[fim+1],fim)
	print("\n\n")
"""

#Índices do log de entrada por cômodo
sala = [2,15,27]
cozinha = [3,7,16,28]
lavanderia = [4,17,29]
escada = [5]
garagem = [6,18]
cobertura = [11,21]
corredor = [12,22]
quarto1 = [8,19,24]
quarto2 = [9,20,25]
quarto3 = [14,23,26]
banheiro = [13]
aquario = [10]

casa = [sala, cozinha, lavanderia, escada, garagem, cobertura, corredor, quarto1, quarto2, quarto3, banheiro, aquario]


############################### dados de acesso na casa #################################

dados_acesso =[]
dias_acesso = [] #Índice no qual um dia acaba

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
	datetime_dia = datetime.strptime(dados_acesso[i][1][:10], '%Y/%m/%d')
	datetime_prox_dia = datetime.strptime(dados_acesso[i+1][1][:10], '%Y/%m/%d')
	if datetime_prox_dia > datetime_dia:
		dias_acesso.append(i+1)
dias_acesso.append(-1)
print(dias_acesso)

################### Extracao das features para classificacao #######################
indice = transicoes[3][1]
#vetor = [dados_casa[:indice][2],dados_casa[:indice][15],dados_casa[:indice][27]]
segmento = dados_casa[:indice] 
vetor = []
for i in segmento:
	aux = [i[2],i[15],i[27]]
	vetor.append(aux)

print(vetor)

#def feature_vector(vetor):

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
from datetime import datetime 
from datetime import time
from operator import itemgetter 
from math import ceil

dados = []

def init_dados(nome):
    global dados
    arquivo = open(nome, "r")
    line = arquivo.readline()
    linesplit = line.split(" ")
    linesplit[-1] = linesplit[-1][:-1]
    del linesplit[-4:-2]
    linesplit[0] = datetime.strptime(linesplit[0], "%m/%d/%Y")
    hora = linesplit[1]
    hora = hora.split(":")
    if linesplit[2] == "PM":
        linesplit[1] = time(int(hora[0]) + 12,int(hora[1]),int(hora[2]))
    else:
        linesplit[1] = time(int(hora[0]),int(hora[1]),int(hora[2]))
    dados.append(linesplit)
    for line in arquivo:
        linesplit = line.split(" ")
        linesplit[-1] = linesplit[-1][:-1]
        if len(linesplit) == 7:
            del linesplit[-4:-2]
        else:
            del linesplit[-3]
        linesplit[0] = datetime.strptime(linesplit[0], "%m/%d/%Y")
        hora = linesplit[1]
        hora = hora.split(":")
        if linesplit[2] == "PM":
            if hora[0] != "12":
                linesplit[1] = time(int(hora[0]) + 12,int(hora[1]),int(hora[2]))
            else:
                linesplit[1] = time(int(hora[0]),int(hora[1]),int(hora[2]))

        elif linesplit[2] == "AM":
            if hora[0] == "12":
                linesplit[1] = time(0,int(hora[1]),int(hora[2]))
            else:
                linesplit[1] = time(int(hora[0]),int(hora[1]),int(hora[2]))
        else:
            print("erro")
            print(line)
            print(linesplit)
        if linesplit != dados[-1]:
            dados.append(linesplit)
    
            
init_dados("march.in")
init_dados("april.in")

####################### sensores ###########################
sensores = []
sensores.append(dados[0][-2])
for elemento in dados:
    add = True
    for sensor in sensores:
        if elemento[-2] == sensor:
            add = False
            break
    if add:
        sensores.append(elemento[-2])

################## separacao dos dados em dias #################
matrix_dados = []
ultimo_dia = dados[-1][0]
dados_dia = []
matrix_dados_aux = []
dados_dia_aux = []
for i in range(len(dados)):
    dia_atual = dados[i][0]
    dia_seguinte = dados[i+1][0]
    dados_dia_aux.append(dados[i])
    if dados[i][-1] == "ON":
        dados_dia.append(2*sensores.index(dados[i][-2]) + 1)
    elif dados[i][-1] == "OFF":
        dados_dia.append(2*sensores.index(dados[i][-2]))
    if dia_atual == ultimo_dia:
        matrix_dados.append(dados_dia)
        matrix_dados_aux.append(dados_dia_aux)
        dados_dia_aux = []
        break
    elif dia_atual < dia_seguinte:
        matrix_dados.append(dados_dia)
        matrix_dados_aux.append(dados_dia_aux)
        dados_dia_aux = []
        dados_dia = []


######################## algoritmo AprioriAll#################

#min_sup = 0.5 #minimum support

def AprioriAll(matrix_dados, min_sup, large1):
    minimo_suporte = ceil(len(matrix_dados)*min_sup)
    list_candidatos = []
    list_candidatos.append(large1) #lista que contem os possiveis candidatos a patterns e seus suportes
    list_candidatos.append([0]*len(large1))
    seq_max = [] #lista que contem todos os patterns 

    #passo k = 1
    for elemento in large1:
        for dia in matrix_dados:
            if elemento in dia:
                list_candidatos[1][large1.index(elemento)] += 1

    seq = []
    seq += [list_candidatos[0].copy()]
    seq += [list_candidatos[1].copy()]
    for candidato in large1:
        indice = seq[0].index(candidato)
        if seq[1][indice] < minimo_suporte:
            del seq[1][indice]
            del seq[0][indice]

    #passo k = 2 
    list_candidatos = [[]]
    for i in range(len(seq[0])):
        for j in range(len(seq[0])):
            if i != j:
                list_candidatos[0].append([seq[0][i],seq[0][j]])
    list_candidatos.append([0]*len(list_candidatos[0]))
    for candidato in list_candidatos[0]:
        for dia in matrix_dados:
            indice = 0
            for evento in dia:
                if candidato[indice] == evento:
                    indice += 1
                    if indice == len(candidato):
                        #indice_candidato = list_candidatos[0].index(candidato)
                        list_candidatos[1][list_candidatos[0].index(candidato)] += 1
                        break 
    seq = []
    seq += [list_candidatos[0].copy()]
    seq += [list_candidatos[1].copy()]
    for candidato in list_candidatos[0]:
        indice = seq[0].index(candidato)
        if seq[1][indice] < minimo_suporte:
            del seq[1][indice]
            del seq[0][indice]
    seq_max.append(seq[0])

    # passo k
    while True:
        list_candidatos = []
        list_candidatos.append(aprioriGen(seq[0]))
        if len(list_candidatos[0]) == 0:
            break
        list_candidatos.append([0]*len(list_candidatos[0]))
        for candidato in list_candidatos[0]:
            for dia in matrix_dados:
                indice = 0
                for evento in dia:
                    if candidato[indice] == evento:
                        indice += 1
                        if indice == len(candidato):
                            list_candidatos[1][list_candidatos[0].index(candidato)] += 1
                            break 
        seq = []
        seq += [list_candidatos[0].copy()]
        seq += [list_candidatos[1].copy()]

        for candidato in list_candidatos[0]:
            indice = seq[0].index(candidato)
            if seq[1][indice] < minimo_suporte:
                del seq[1][indice]
                del seq[0][indice]

        if len(seq[0]) != 0:
            seq_max.append(seq[0])

    seq = seq_max[-1]
   
    
    for i in range(len(seq_max)-1):
        list_candidatos = seq_max[i].copy() # lista de candidatos a patterns
        for candidato in seq_max[i]:
            indice = 0
            presente = False #flag para indicar se um pattern menor esta presente em um pattern maior
            for maior_seq in seq:
                if presente:
                    break
                for evento in maior_seq:
                    if candidato[indice] == evento:
                        indice += 1
                        if indice == len(candidato):
                            presente = True
                            del list_candidatos[list_candidatos.index(candidato)]
                            break
        seq_max[i] = list_candidatos.copy()

            
    return seq_max
    
    
        


def aprioriGen(list_seq):
    lista_candidato = []
    for i in range(len(list_seq)):
        for j in range(len(list_seq)):
            if list_seq[i][0:-1] ==  list_seq[j][0:-1] and i!=j:
                lista_candidato.append(list_seq[i] + list_seq[j][-1:])
    lista_retorno = lista_candidato.copy()
    for elemento in lista_candidato:
        for i in range(len(elemento)):
            sub_seq = elemento.copy()
            del sub_seq[i]
            if not(sub_seq in list_seq):
                del lista_retorno[lista_retorno.index(elemento)]
                break
    return lista_retorno

########################################## dados hayashi ##########################################
dados_casa = [] #dados da casa
matrix_casa = [] #dados da casa tratados para usar data mining
arquivo = open("home.csv", "r")

line = arquivo.readline()
lineSplit = line.split(",") 
lineSplit[-1] = lineSplit[-1][:-1]
dados_casa.append(lineSplit)


for line in arquivo:
    lineSplit = line.split(",")
    lineSplit[2:] =  list(map(int,lineSplit[2:])) 
    dados_casa.append(lineSplit)
arquivo.close()
large1 = []
for coluna in range(2,len(dados_casa[0])):
    if coluna > 14 and coluna < 24 and coluna != 19:
        valor_atual = dados_casa[1][coluna]
        prox_valor = dados_casa[2][coluna]
        if prox_valor < valor_atual or valor_atual < 50:
            matrix_casa.append([dados_casa[0][coluna], dados_casa[1][1]])
        large1.append(dados_casa[0][coluna])
    elif coluna != 19:
        if dados_casa[1][coluna] == 0:
            matrix_casa.append([dados_casa[0][coluna] + " OFF", dados_casa[1][1]])
        elif dados_casa[1][coluna] == 1:
            matrix_casa.append([dados_casa[0][coluna] + " ON", dados_casa[1][1]])
        else:
            print("Erro")
            break
        large1.append(dados_casa[0][coluna] + " ON")
        large1.append(dados_casa[0][coluna] + " OFF")
for linha in range(3,len(dados_casa)-1):
    for coluna in range(2, len(dados_casa[0])):
        if coluna > 14 and coluna < 24 and coluna != 19:
            valor_atual = dados_casa[linha][coluna]
            prox_valor = dados_casa[linha + 1][coluna]
            if prox_valor < valor_atual or valor_atual < 50:
                matrix_casa.append([dados_casa[0][coluna], dados_casa[linha][1]])
        elif coluna != 19:
            valor_atual = dados_casa[linha][coluna]
            valor_anterior = dados_casa[linha - 1][coluna]
            if valor_atual == 0 and valor_atual != valor_anterior:
                matrix_casa.append([dados_casa[0][coluna] + " OFF", dados_casa[linha][1]])
            elif valor_atual == 1 and valor_atual != valor_anterior:
                matrix_casa.append([dados_casa[0][coluna] + " ON", dados_casa[linha][1]])
            elif valor_atual != 0 and valor_atual != 1:
                print("Erro")
                break
dados_dia = [] # matrix separada em dias
dados_dia_aux = [] # matrix auxiliar para separar em dias
for i in range(len(matrix_casa) -1): #verifica se os elementos estão em ordem e separa a matrix em dias
    atual = datetime.strptime(matrix_casa[i][1][1:-1], "%Y-%m-%d %H:%M") # hora atual para verificar a ordem
    depois = datetime.strptime(matrix_casa[i+1][1][1:-1], "%Y-%m-%d %H:%M") # hora atual + 1 para verificar a ordem
    dia_atual = datetime.strptime(matrix_casa[i][1][1:11], '%Y-%m-%d')
    dia_seguinte = datetime.strptime(matrix_casa[i+1][1][1:11], '%Y-%m-%d')
    
    dados_dia_aux.append(matrix_casa[i][0])
    if dia_atual < dia_seguinte:
        dados_dia.append(dados_dia_aux)
        dados_dia_aux = []
    if i == len(matrix_casa) -2:
        dados_dia_aux.append(matrix_casa[i][0])
        dados_dia.append(dados_dia_aux)
    if atual > depois:
        print("erro na matrix_casa indice: ",i)


eventos = AprioriAll(dados_dia, 1,large1) #patterns encontrados
print(eventos)
print("a")



########################################## dados artigo ##########################################

#test = [[1,5,2,3,4],[1,3,4,3,5],[1,2,3,4],[1,3,5],[4,5]]
#a = AprioriAll(test,0.6,[1,2,3,4,5])
'''
large1 = []
for i in range(max(max(matrix_dados))+1):
    large1.append(i)
eventos = AprioriAll(matrix_dados,0.45,large1)
        
 


eventos_sensor = []
for seq in eventos:
    for i in range(len(seq)):
        aux = []
        for indice_sensor in seq[i]:
            if (indice_sensor%2) == 0:
                aux.append(sensores[int(indice_sensor/2)])
            else:
                aux.append(sensores[int((indice_sensor-1)/2)])
        eventos_sensor.append(aux)
print("a")


frequencia = [0]*len(sensores)
for elemento in dados:
    for sensor in sensores:
        if elemento[-2] == sensor:
            indice = sensores.index(sensor)
            frequencia[indice] += 1
dic = {}
for i in range(len(frequencia)):
    dic[sensores[i]] = frequencia[i]
frequencia = sorted(dic.items(),key=itemgetter(1))
media = 0
for valor in dic.values():
    media += valor
media = media/len(dic)
#for elemento in frequencia:
#    print(elemento)
print("\n\n", media)

'''
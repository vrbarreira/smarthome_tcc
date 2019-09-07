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
    if dados[i][-2] == "A12":
        print("a")
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

min_sup = 0.5 #minimum support

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

#test = [[1,5,2,3,4],[1,3,4,3,5],[1,2,3,4],[1,3,5],[4,5]]
#a = AprioriAll(test,0.6,[1,2,3,4,5])

large1 = []
for i in range(max(max(matrix_dados))+1):
    large1.append(i)
eventos = AprioriAll(matrix_dados,0.45,large1)
        
 
#test = [[1,2,3],[1,2,4],[1,3,4],[1,3,5],[2,3,4]]
#seq = aprioriGen(test)
#print(aprioriGen(seq))

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
print(eventos_sensor)


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
#print("\n\n", media)


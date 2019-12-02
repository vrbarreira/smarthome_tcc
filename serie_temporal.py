from datetime import datetime 
from datetime import time
from datetime import timedelta
from operator import itemgetter 
from math import ceil
from random import randint
import numpy as np

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

################## separacao dos dados do artigo em dias #################
matrix_dados = []
ultimo_dia = dados[-1][0]
dados_dia = []
matrix_dados_aux = []
dados_dia_aux = []
for i in range(len(dados)):
    dia_atual = dados[i][0]
    dia_seguinte = dados[i+1][0]
    dados_dia_aux.append(dados[i])
    dados_dia.append(sensores.index(dados[i][-2]))
    '''
    if dados[i][-1] == "ON":
        dados_dia.append(2*sensores.index(dados[i][-2]) + 1)
    elif dados[i][-1] == "OFF":
        dados_dia.append(2*sensores.index(dados[i][-2]))
    '''
    if dia_atual == ultimo_dia:
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

def start_end_time(matrix_dados, eventos):
    start_end_vect = []
    for i in eventos:
        start_end_vect.append([])
    for i in range(len(matrix_dados)):
        if matrix_dados[i][-2] in eventos and matrix_dados[i][-1] == "ON" and i < len(matrix_dados)-1:
            start_time = i #indice no qual o evento comecou
            end_time = i + 1 #indice no qual o evento acaba
            evento = matrix_dados[i][-2] #evento em si
            add = True
            while not(matrix_dados[end_time][-2] == evento and matrix_dados[end_time][-1] == "OFF"):
                if matrix_dados[end_time][-2] == evento and matrix_dados[end_time][-1] == "ON":
                    print("Sensor ligou sem desligar antes")
                    add = False
                    break
                end_time += 1
                if end_time == 16992:
                    print("a")
                if end_time >= len(matrix_dados):
                    print("Sensor não desligou")
                    add = False
                    break
            if add and matrix_dados[start_time][0] == matrix_dados[end_time][0] :
                start_end_vect[eventos.index(evento)].append([matrix_dados[start_time][0],evento,matrix_dados[start_time][1],matrix_dados[end_time][1]])
    
    return start_end_vect

def busca_relacao(vetor, data, hora_inicioX, hora_fimX, threshold_igual):
    limite_inferior = 0 #limite inferior para a busca da faixa de horarios
    limite_superior = len(vetor) #limite superior para a busca da faixa de horarios
    indice_atual = int(len(vetor)/2) #indice inicial para a busca do horario correspondente no vetor dados_acesso

    threshold_rel = timedelta(minutes=5) #limite para considerar que existe relacao temporal entre os eventos
    tempo_zero = timedelta(minutes=0)
    while True:
        #data_atual = vetor[indice_atual][0].date() #data em que a busca se encontra para os dados do artigo
        data_atual = vetor[indice_atual][0] #data em que a busca se encontra para os dados do hayashi
        hora_inicioY = datetime.combine(data_atual, vetor[indice_atual][-2]) #tempo de inicio do evento em que a busca se encontra
        hora_fimY = datetime.combine(data_atual, vetor[indice_atual][-1]) # tempo de fim do evento em que a busca se encontra
        if data_atual == data:

            if abs(hora_inicioX - hora_inicioY) < threshold_igual or abs(hora_fimX - hora_fimY)< threshold_igual: #o inicio eh igual ou o fim eh igual (start,startBy,equal,finish,finishedBy)
                if abs(hora_inicioX - hora_inicioY) < threshold_igual and abs(hora_fimX - hora_fimY)< threshold_igual: #(equals)
                    return 1
                elif abs(hora_fimX - hora_fimY) < threshold_igual and (hora_inicioX - hora_inicioY) < tempo_zero: #(finishedBy)
                    return 5
                elif abs(hora_fimX - hora_fimY) < threshold_igual and (hora_inicioX - hora_inicioY) > tempo_zero: #(finish)
                    return 6
                elif abs(hora_inicioX - hora_inicioY) < threshold_igual and (hora_fimX - hora_fimY) > tempo_zero: #(startedBy)
                    return 7
                elif abs(hora_inicioX - hora_inicioY) < threshold_igual and (hora_fimX - hora_fimY) < tempo_zero: #(start)
                    return 8 
                
                    
            elif hora_inicioY - hora_fimX < threshold_rel and hora_inicioY - hora_fimX > tempo_zero : #o evento em questao esta antes de um outro evento (before)
                return 2
            elif hora_inicioX - hora_inicioY < tempo_zero and hora_fimY - hora_fimX < tempo_zero: #contains
                return 4
            elif abs(hora_fimX - hora_inicioY) < threshold_igual: #(meets)
                return 9
            elif hora_inicioX < hora_inicioY and hora_inicioY < hora_fimX and hora_fimX < hora_fimY: #(overlaps)
                return 3
                

            #vetor_retorno.append(vetor[indice_atual])
       
        if (hora_inicioY - hora_inicioX)  < tempo_zero : #hora_inicioX esta depois de hora_inicioY
            prox_indice = int((indice_atual + limite_superior)/2)
            limite_inferior = indice_atual

        elif (hora_inicioY - hora_inicioX) > tempo_zero: #hora_inicioX esta antes de hora_inicioY
            prox_indice = int((indice_atual + limite_inferior)/2)
            limite_superior = indice_atual
       
        if prox_indice == indice_atual:
            return None
        indice_atual = prox_indice
            
def relacao_temporal(start_end_vect_eventoX, start_end_vect_eventoY):
    resultado = [["sensor relacionado","start","startedBy","equals","finish","finishedBy","meets","overlaps","contains","before"]]
    threshold = timedelta(minutes=2) #limite para considerar que o timestamp dos eventos sao iguais
    resultado.append([0]*9)
    resultado[1].insert(0,start_end_vect_eventoY[0][1])
    for evento in start_end_vect_eventoX:
        #data = evento[0].date() #para os dados do artigo
        data = evento[0] # para os dados do hayashi
        hora_inicioX = datetime.combine(data, evento[2]) 
        hora_fimX = datetime.combine(data, evento[3]) 
        tipo = busca_relacao(start_end_vect_eventoY, data,hora_inicioX,hora_fimX, threshold) #contem o evento que sera avaliado na relacao temporal

        if tipo == 1:
            rel_temporal = resultado[0].index("equals") 
            resultado[1][rel_temporal] += 1
        elif tipo == 2:
            rel_temporal = resultado[0].index("before") 
            resultado[1][rel_temporal] += 1
        elif tipo == 3:
            rel_temporal = resultado[0].index("overlaps") 
            resultado[1][rel_temporal] += 1
        elif tipo == 4:
            rel_temporal = resultado[0].index("contains") 
            resultado[1][rel_temporal] += 1
        elif tipo == 5:
            rel_temporal = resultado[0].index("finishedBy") 
            resultado[1][rel_temporal] += 1
        elif tipo == 6:
            rel_temporal = resultado[0].index("finish") 
            resultado[1][rel_temporal] += 1
        elif tipo == 7:
            rel_temporal = resultado[0].index("startedBy") 
            resultado[1][rel_temporal] += 1
        elif tipo == 8:
            rel_temporal = resultado[0].index("start") 
            resultado[1][rel_temporal] += 1
        elif tipo == 9:
            rel_temporal = resultado[0].index("meets") 
            resultado[1][rel_temporal] += 1

    return resultado

def probabilidade(vetor, numero_ocorrencias):
    probabilidade_sensores=[]

    for i in range(len(vetor)):
        tabela_relacao = vetor[i][1].copy()
        sensorX = vetor[i][0]
        for sensor in tabela_relacao:
            soma = 0
            sensorY = sensor[1][0]
            for j in range(1,len(sensor[1])):
                soma += sensor[1][j]
            probabilidade_sensor = soma/numero_ocorrencias[i]
            #probabilidade_sensores.append(["P("+ sensorY +"|" + sensorX + ")",probabilidade_sensor])
            probabilidade_sensores.append([sensorY, sensorX ,probabilidade_sensor])
    return probabilidade_sensores

def busca_probabilidade(sensor_avaliado, sensor_ocorrido, eventos):
    limite_inferior = 0 #limite inferior para a busca da faixa de horarios
    limite_superior = len(eventos) #limite superior para a busca da faixa de horarios
    indice_atual = int(len(eventos)/2) #indice inicial para a busca do horario correspondente no vetor dados_acesso

    while True:
        if sensor_ocorrido == eventos[indice_atual][1]:
            if sensor_avaliado == eventos[indice_atual][0]:
                return indice_atual
            elif sensor_avaliado > eventos[indice_atual][0]:
                prox_indice = int((indice_atual + limite_superior)/2)
                limite_inferior = indice_atual
            elif sensor_avaliado < eventos[indice_atual][0]:
                prox_indice = int((indice_atual + limite_inferior)/2)
                limite_superior = indice_atual

        elif sensor_ocorrido > eventos[indice_atual][1]:
            prox_indice = int((indice_atual + limite_superior)/2)
            limite_inferior = indice_atual
        elif sensor_ocorrido < eventos[indice_atual][1]:
            prox_indice = int((indice_atual + limite_inferior)/2)
            limite_superior = indice_atual
       
        if prox_indice == indice_atual:
            print("combinacao de sensores nao existe")
            return None
        indice_atual = prox_indice


def classificador(start_end_vect, vetor_verificacao, lista_eventos):
    relacoes = []
    numero_ocorrencias = []
    for elemento in start_end_vect:
        relacoes.append([elemento[0][1]])
        numero_ocorrencias.append(len(elemento))
    for x in range(len(start_end_vect)):
        resultado = [] #contem as relacoes de um dado sensorX com todos os outros sensores da base
        for y in range(len(start_end_vect)):
            if x != y:
                #print("sensorX: ", start_end_vect[x][0][1])
                resultado.append(relacao_temporal(start_end_vect[x],start_end_vect[y]))
                #print(resultado[0])
                #print(resultado[1])
        relacoes[x].append(resultado)


    probabilidades_eventos = probabilidade(relacoes,numero_ocorrencias) #contem a probabilidades dos eventos Y ocorrerem dado q ocorreu um evento X
    valores_anormais = [] #valor de anormalidade de um evento Y dado que X ocorreu
    valores_anormais_busca = []# vetor auxiliar para buscar o valor de anormalidade de Y
    probabilidades_valores = []# vetor que contem apenas as probabilidades do vetor "valores_anormais"



    for elemento in probabilidades_eventos:
        valores_anormais.append([elemento[0],elemento[1],1-elemento[2]])
        valores_anormais_busca.append([lista_eventos.index(elemento[0]),lista_eventos.index(elemento[1])])
        probabilidades_valores.append(1 - elemento[2])
    desv_pad = np.std(probabilidades_valores)
    media = np.mean(probabilidades_valores)
    threshold_ocorrido = media + 2 * desv_pad
    if threshold_ocorrido > 1.0:
        threshold_ocorrido = 1.0 
    for ind_ultimo_dia in range(len(dados)):
        if dados[ind_ultimo_dia][0] == ultimo_dia:
            break


    eventos_ocorridos = []
    indice = 0
    classificacao = [["evento","timestamp", "probabilidade do evento", "valor de anormalidade","detectada anomalia"]]
    while True:
        sensor_avaliado = vetor_verificacao[indice][-2]
        if sensor_avaliado in lista_eventos and sensor_avaliado not in eventos_ocorridos and vetor_verificacao[indice][-1] == "ON":
            eventos_ocorridos.append(sensor_avaliado)
        if len(eventos_ocorridos) == 2:
            evento_avaliado = eventos_ocorridos[-1]
            evento_ocorrido = eventos_ocorridos[-2]
            indice_anormalidade = busca_probabilidade(lista_eventos.index(evento_avaliado),lista_eventos.index(evento_ocorrido),valores_anormais_busca) # indice no qual se encontra a probabilidade buscada
            timeStamp = vetor_verificacao[indice][2]
            if valores_anormais[indice_anormalidade][2] >= threshold_ocorrido:
                classificacao.append([evento_avaliado,timeStamp,probabilidades_eventos[indice_anormalidade][2], valores_anormais[indice_anormalidade][2], "SIM"])
            else:
                classificacao.append([evento_avaliado,timeStamp,probabilidades_eventos[indice_anormalidade][2], valores_anormais[indice_anormalidade][2],"NAO"])
            break
        indice +=1
        if indice == len(vetor_verificacao):
            print("nao occoreram eventos frequentes")
            break

    for i in range(indice, len(vetor_verificacao)):
        sensor_avaliado = vetor_verificacao[i][-2]
        if sensor_avaliado in lista_eventos and sensor_avaliado != eventos_ocorridos[-1] and vetor_verificacao[i][-1] == "ON":
            eventos_ocorridos.append(sensor_avaliado)
            evento_avaliado = eventos_ocorridos[-1]
            evento_ocorrido = eventos_ocorridos[-2]
            timeStamp = vetor_verificacao[i][2]
            indice_anormalidade = busca_probabilidade(lista_eventos.index(evento_avaliado),lista_eventos.index(evento_ocorrido),valores_anormais_busca) # indice no qual se encontra a probabilidade buscada
            if valores_anormais[indice_anormalidade][2] >= threshold_ocorrido:
                classificacao.append([evento_avaliado,timeStamp,probabilidades_eventos[indice_anormalidade][2], valores_anormais[indice_anormalidade][2], "SIM"])
            else:
                classificacao.append([evento_avaliado,timeStamp,probabilidades_eventos[indice_anormalidade][2], valores_anormais[indice_anormalidade][2],"NAO"])
    return classificacao,threshold_ocorrido, media, desv_pad

def prob_uniao(eventos_ocorridos, probabilidades_eventos, lista_probabilidade):
    my_set = [False]*len(conjunto)
    subconjuntos = []
    gera_subconjunto(0,my_set,eventos_ocorridos,subconjuntos)
    
def gera_subconjunto(k,my_set, conjunto, subconjuntos):
    if k== len(conjunto):
        subconjunto = []
        for i in range(len(my_set)):
            if my_set[i]:
                subconjunto.append(conjunto[i])
        if len(subconjunto)>= 2:
            subconjuntos.append(subconjunto)
    else:
        my_set[k] = True
        gera_subconjunto(k + 1, my_set,conjunto,subconjuntos)
        my_set[k] = False
        gera_subconjunto(k + 1, my_set,conjunto,subconjuntos)

coisa = []
conjunto =[1,2,3,4]
my_set = [False]*len(conjunto)
gera_subconjunto(0,my_set,conjunto,coisa)
print("a")

def probabilidade_eventoX(probabilidade_ocorridos, eventos_ocorridos,lista_eventos,valores_anormais_busca, probabilidades_eventos):
    evento_ocorrido_A = eventos_ocorridos[-3]
    P_A = probabilidade_ocorridos[-2]
    evento_ocorrido_B = eventos_ocorridos[-2]
    P_B = probabilidade_ocorridos[-1]
    evento_avaliado = eventos_ocorridos[-1]
    indice_XA = busca_probabilidade(lista_eventos.index(evento_avaliado),lista_eventos.index(evento_ocorrido_A),valores_anormais_busca) # indice no qual se encontra a probabilidade buscada
    indice_XB = busca_probabilidade(lista_eventos.index(evento_avaliado),lista_eventos.index(evento_ocorrido_B),valores_anormais_busca) # indice no qual se encontra a probabilidade buscada
    if indice_XA != None:
        indice_AB = busca_probabilidade(lista_eventos.index(evento_ocorrido_A),lista_eventos.index(evento_ocorrido_B),valores_anormais_busca) # indice no qual se encontra a probabilidade buscada
        P_XA = probabilidades_eventos[indice_XA][2]
        P_XB = probabilidades_eventos[indice_XB][2]
        P_AB = probabilidades_eventos[indice_AB][2]
        P_AB_B = P_AB * P_B
        probabilidade_X = (P_XA * P_A + P_XB * P_B)/ (P_A + P_B - P_AB_B)
    else: 
        probabilidade_X = probabilidades_eventos[indice_XB][2]
    if probabilidade_X > 1.0:
        probabilidade_X = 1.0
    probabilidade_ocorridos.append(probabilidade_X)
    return probabilidade_X

probabilidades_eventos = []

def classificador2_0(start_end_vect, vetor_verificacao, lista_eventos):
    relacoes = []
    numero_ocorrencias = []
    global probabilidades_eventos
    for elemento in start_end_vect:
        relacoes.append([elemento[0][1]])
        numero_ocorrencias.append(len(elemento))
    for x in range(len(start_end_vect)):
        resultado = [] #contem as relacoes de um dado sensorX com todos os outros sensores da base
        for y in range(len(start_end_vect)):
            if x != y:
                #print("sensorX: ", start_end_vect[x][0][1])
                resultado.append(relacao_temporal(start_end_vect[x],start_end_vect[y]))
                #print(resultado[0])
                #print(resultado[1])
        relacoes[x].append(resultado)


    probabilidades_eventos = probabilidade(relacoes,numero_ocorrencias) #contem a probabilidades dos eventos Y ocorrerem dado q ocorreu um evento X
    valores_anormais = [] #valor de anormalidade de um evento Y dado que X ocorreu
    valores_anormais_busca = []# vetor auxiliar para buscar o valor de anormalidade de Y
    probabilidades_valores = []# vetor que contem apenas as probabilidades do vetor "valores_anormais"
    
    for elemento in probabilidades_eventos:
        valores_anormais.append([elemento[0],elemento[1],1-elemento[2]])
        valores_anormais_busca.append([lista_eventos.index(elemento[0]),lista_eventos.index(elemento[1])])
        probabilidades_valores.append(1 - elemento[2])
    desv_pad = np.std(probabilidades_valores)
    media = np.mean(probabilidades_valores)
    threshold_ocorrido = media + 2 * desv_pad
    if threshold_ocorrido > 1.0:
        threshold_ocorrido = 1.0 
    for ind_ultimo_dia in range(len(dados)):
        if dados[ind_ultimo_dia][0] == ultimo_dia:
            break

    eventos_ocorridos = []
    probabilidade_ocorridos =[] # probabilidade do evento ocorrer para os eventos ocorridos
    indice = 0
    classificacao = [["evento","timestamp", "probabilidade do evento", "valor de anormalidade","detectada anomalia"]]
    entra = False
    while len(eventos_ocorridos) < 3:
        sensor_avaliado = vetor_verificacao[indice][-2]
        if len(eventos_ocorridos) == 0:
            if sensor_avaliado in lista_eventos and vetor_verificacao[indice][-1] == "ON":
                eventos_ocorridos.append(sensor_avaliado)
        elif sensor_avaliado in lista_eventos and sensor_avaliado != eventos_ocorridos[-1] and vetor_verificacao[indice][-1] == "ON":
            eventos_ocorridos.append(sensor_avaliado)
            entra = True
        if len(eventos_ocorridos) >= 2 and entra:
            evento_avaliado = eventos_ocorridos[-1]
            evento_ocorrido = eventos_ocorridos[-2]
            indice_anormalidade = busca_probabilidade(lista_eventos.index(evento_avaliado),lista_eventos.index(evento_ocorrido),valores_anormais_busca) # indice no qual se encontra a probabilidade buscada
            timeStamp = vetor_verificacao[indice][2]
            if valores_anormais[indice_anormalidade][2] >= threshold_ocorrido:
                classificacao.append([evento_avaliado,timeStamp,probabilidades_eventos[indice_anormalidade][2], valores_anormais[indice_anormalidade][2], "SIM"])
                probabilidade_ocorridos.append(probabilidades_eventos[indice_anormalidade][2])
            else:
                classificacao.append([evento_avaliado,timeStamp,probabilidades_eventos[indice_anormalidade][2], valores_anormais[indice_anormalidade][2],"NAO"])
                probabilidade_ocorridos.append(probabilidades_eventos[indice_anormalidade][2])
            entra = False
        indice +=1
        if indice == len(vetor_verificacao):
            print("nao occoreram eventos frequentes")
            break
    for i in range(indice, len(vetor_verificacao)):
        sensor_avaliado = vetor_verificacao[i][-2]
        if sensor_avaliado in lista_eventos and sensor_avaliado != eventos_ocorridos[-1] and vetor_verificacao[i][-1] == "ON":
            eventos_ocorridos.append(sensor_avaliado)
            P_X = probabilidade_eventoX(probabilidade_ocorridos, eventos_ocorridos,lista_eventos,valores_anormais_busca, probabilidades_eventos)
            timeStamp = vetor_verificacao[indice][2]
            if (1 - P_X) >= threshold_ocorrido:
                classificacao.append([sensor_avaliado,timeStamp, P_X, 1 - P_X, "SIM"])
            else:
                classificacao.append([sensor_avaliado,timeStamp, P_X, 1 - P_X,"NAO"])
    return classificacao,threshold_ocorrido, media, desv_pad

            
def dia_teste(matrix_casa, dia):
    inicio_encontrado = False
    indice_inicial = 0
    indice_final = len(matrix_casa)
    for i in range(len(matrix_casa)):
        if matrix_casa[i][0] == dia and not(inicio_encontrado):
            indice_inicial = i
            inicio_encontrado = True
        elif matrix_casa[i][0] != dia and inicio_encontrado:
            indice_final = i
            break
    treino = matrix_casa.copy()
    teste = matrix_casa[indice_inicial:indice_final]
    del treino[indice_inicial:indice_final]
    return treino, teste
    
########################################## dados hayashi ##########################################

patterns = []
def init_patterns():
    global patterns
    arquivo_patterns = open("patterns.txt", "r")
    for line in arquivo_patterns:
        linesplit = line.split(",")
        patterns.append(linesplit[:-1])
    arquivo_patterns.close()

def read_arq(name, matrix_casa, dados_casa):
    arquivo = open(name, "r")
    lines = arquivo.readlines()
    lineSplit = lines[0].split(",") 
    lineSplit[-1] = lineSplit[-1][:-1]
    dados_casa.append(lineSplit)


    for line in lines[1:]:
        lineSplit = line.split(",")
        lineSplit[2:] =  list(map(int,lineSplit[2:])) 
        dados_casa.append(lineSplit)
    arquivo.close()
    #large1 = []
    flag_presenca = [False]* len(dados_casa[0])
    for coluna in range(2,len(dados_casa[0])):
        #dia = datetime.strptime(dados_casa[1][1][1:-1], "%Y-%m-%d %H:%M") # hora atual para verificar a ordem
        dia = datetime.strptime(dados_casa[1][1], "%Y-%m-%d %H:%M") # hora atual para verificar a ordem
        hora = time(dia.hour,dia.minute)
        valor_atual = dados_casa[1][coluna]
        if coluna > 14 and coluna < 24 and coluna != 19:
            if valor_atual < 100:
                matrix_casa.append([dia.date(),hora,dados_casa[1][1],dados_casa[0][coluna],"ON" ])
                flag_presenca[coluna] = True
            elif valor_atual > 100:
                matrix_casa.append([dia.date(),hora,dados_casa[1][1],dados_casa[0][coluna],"OFF" ])
                flag_presenca[coluna] = False
            #large1.append(dados_casa[0][coluna])
        elif coluna != 19:
            if valor_atual == 0:
                matrix_casa.append([dia.date(),hora,dados_casa[1][1],dados_casa[0][coluna], "OFF"])
            elif valor_atual == 1:
                matrix_casa.append([dia.date(),hora,dados_casa[1][1], dados_casa[0][coluna], "ON"])
            else:
                print("Erro")
                break
            #large1.append(dados_casa[0][coluna])
    for linha in range(2,len(dados_casa)-1):
        for coluna in range(2, len(dados_casa[0])):
            #dia = datetime.strptime(dados_casa[linha][1][1:-1], "%Y-%m-%d %H:%M") # hora atual para verificar a ordem
            dia = datetime.strptime(dados_casa[linha][1], "%Y-%m-%d %H:%M") # hora atual para verificar a ordem
            hora = time(dia.hour,dia.minute)
            if coluna > 14 and coluna < 24 and coluna != 19:
                valor_atual = dados_casa[linha][coluna]
                prox_valor = dados_casa[linha + 1][coluna]
                if prox_valor < valor_atual and valor_atual > 100 and not flag_presenca[coluna]:
                    matrix_casa.append([dia.date(),hora,dados_casa[linha][1],dados_casa[0][coluna],"ON" ])
                    flag_presenca[coluna] = True
                elif prox_valor > valor_atual and prox_valor > 100 and valor_atual < 100  and flag_presenca[coluna]:
                    matrix_casa.append([dia.date(),hora,dados_casa[linha][1],dados_casa[0][coluna],"OFF" ])
                    flag_presenca[coluna] = False
            elif coluna != 19:
                valor_atual = dados_casa[linha][coluna]
                valor_anterior = dados_casa[linha - 1][coluna]
                if valor_atual == 0 and valor_atual != valor_anterior:
                    matrix_casa.append([dia.date(),hora,dados_casa[linha][1], dados_casa[0][coluna], "OFF"])
                elif valor_atual == 1 and valor_atual != valor_anterior:
                    matrix_casa.append([dia.date(),hora,dados_casa[linha][1], dados_casa[0][coluna], "ON"])
                elif valor_atual != 0 and valor_atual != 1:
                    print("Erro")
                    break

dados_casa = [] #dados da casa
matrix_casa = [] #dados da casa tratados para usar na serie temporal

read_arq("home_sem_aspa.csv", matrix_casa, dados_casa)

dados_dia = [] # dados formatados para o datamining separados em dias
dados_dia_aux = [] # auxilia na formatacao dos dados para o datamining
matrix_casa_aux = [] # auxlia na separacao dos dados em dias
matrix_casa_dia = [] # dados separados em dias
for i in range(len(matrix_casa) -1): #verifica se os elementos estão em ordem e separa a matrix em dias
    #atual = datetime.strptime(matrix_casa[i][2][1:-1], "%Y-%m-%d %H:%M") # hora atual para verificar a ordem
    #depois = datetime.strptime(matrix_casa[i+1][2][1:-1], "%Y-%m-%d %H:%M") # hora atual + 1 para verificar a ordem
    atual = datetime.strptime(matrix_casa[i][2], "%Y-%m-%d %H:%M") # hora atual para verificar a ordem
    depois = datetime.strptime(matrix_casa[i+1][2], "%Y-%m-%d %H:%M") # hora atual + 1 para verificar a ordem
    if  matrix_casa[i][-1] == "ON":
        dados_dia_aux.append(matrix_casa[i][-2])
    matrix_casa_aux.append(matrix_casa[i])
    

    if atual.date() < depois.date():
        dados_dia.append(dados_dia_aux)
        matrix_casa_dia.append(matrix_casa_aux)
        dados_dia_aux = []
        matrix_casa_aux = []
    if i == len(matrix_casa) -2:
        dados_dia_aux.append(matrix_casa[i][-2])
        matrix_casa_dia.append(matrix_casa_aux)
        dados_dia.append(dados_dia_aux)
        matrix_casa_aux = []
    if atual > depois:
        print("erro na matrix_casa indice: ",i)

"""
eventos = AprioriAll(dados_dia, 0.95,large1) #patterns encontrados
print(eventos)
arq_saida = open("patterns.txt", "w+")
for sequencia_N in eventos:
    for vetor in sequencia_N:
        for elemento in vetor:
            arq_saida.write(elemento)
            arq_saida.write(",")
        arq_saida.write("\n")    
arq_saida.close()
"""

init_patterns()

lista_eventos = []
for seq in patterns:
    for sensor in seq:
        if sensor not in lista_eventos:
            lista_eventos.append(sensor)

ultimo_dia = matrix_casa[-1][0]
for i in range(len(matrix_casa)):
    if matrix_casa[i][0] == ultimo_dia:
        indice_ultimo_dia = i
        break

#vetor_verificacao = matrix_casa[indice_ultimo_dia:].copy()
#matrix_casa_relacoes = matrix_casa[:indice_ultimo_dia]

##########################################teste cenarios ############################################
teste_invasao = []
teste_visita = []

read_arq("invasao.csv",teste_invasao,[])
read_arq("visita.csv",teste_visita,[])

matrix_casa_relacoes, vetor_verificacao= dia_teste(matrix_casa, matrix_casa[-1][0])

start_end_vect = start_end_time(matrix_casa_relacoes, lista_eventos)
'''
vetor_teste = []
dia = vetor_verificacao[0][0]
hora = vetor_verificacao[0][1]
data = vetor_verificacao[0][2]
for elemento in vetor_verificacao:
    if  elemento[-2] in lista_eventos:
        evento = lista_eventos[randint(0,len(lista_eventos)-1)]
        elemento[-2] = evento
    vetor_teste.append(elemento)
'''

vetor_teste_N_2 = []
dia = vetor_verificacao[0][0]
hora = vetor_verificacao[0][1]
data = vetor_verificacao[0][2]
for eventoA in lista_eventos:
    for eventoB in lista_eventos:
        for evento_ocorrido in lista_eventos:
            if evento_ocorrido != eventoB:
                vetor_teste_N_2.append([dia,hora,data,eventoA,'ON'])
                vetor_teste_N_2.append([dia,hora,data,eventoB,'ON'])
                vetor_teste_N_2.append([dia,hora,data,evento_ocorrido,'ON'])

resultado_N2,threshold_ocorrido, media, desv_pad = classificador2_0(start_end_vect, vetor_teste_N_2, lista_eventos)

resultado1,threshold, media, desv_pad = classificador(start_end_vect, vetor_verificacao, lista_eventos)
resultado2,threshold, media, desv_pad = classificador2_0(start_end_vect, vetor_verificacao, lista_eventos)
resultado_invasao, threshold, media, desv_pad = classificador2_0(start_end_vect, teste_invasao, lista_eventos)
resultado_visita, threshold, media_hist_N_1, desv_pad_hist_N_1 = classificador2_0(start_end_vect, teste_visita, lista_eventos)

def calc_estatisticas(resultado):
    prob_result = []
    for elemento in resultado[1:]:
        prob_result.append(elemento[3])
    
    desv_pad = np.std(prob_result)
    media = np.mean(prob_result)
    return desv_pad, media

def analisa_resultado(resultado):
    avaliacao_anormal =[]
    valores_anormais_faixa = [["0 - 20", "21 - 40", "41 - 60", "61 - 80", "81+"],[0,0,0,0,0]]
    maior_valor_anormal = 0
    valores_anormais = []
    numero_alertas = [0,0,0]
    log = []
    for avaliacao in resultado[1:]:
        if avaliacao[-1] == "SIM":
            avaliacao_anormal.append(avaliacao)
        if avaliacao[-2] > maior_valor_anormal:
            maior_valor_anormal = avaliacao[-2]
            valores_anormais.append(avaliacao)
        if avaliacao[-2] > 0.8 and avaliacao[-2] <= 0.89:
            numero_alertas[0] += 1
            log.append(avaliacao)
        elif avaliacao[-2] > 0.89 and avaliacao[-2] <= threshold:
            numero_alertas[1] += 1
            log.append(avaliacao)
        elif avaliacao[-2] > threshold:
            numero_alertas[2] += 1
            log.append(avaliacao)
        if avaliacao[-2] <= 0.2:
            valores_anormais_faixa[1][0] += 1
        elif avaliacao[-2] > 0.2 and avaliacao[-2] <= 0.4:
            valores_anormais_faixa[1][1] += 1
        elif avaliacao[-2] > 0.4 and avaliacao[-2] <= 0.6:
            valores_anormais_faixa[1][2] += 1
        elif avaliacao[-2] > 0.6 and avaliacao[-2] <= 0.8:
            valores_anormais_faixa[1][3] += 1
        elif avaliacao[-2] > 0.8:
            valores_anormais_faixa[1][4] += 1
    return avaliacao_anormal, valores_anormais_faixa, valores_anormais, numero_alertas, log

desv_pad_N_1 = []
media_N_1 = [] 
desv_pad_N_2 = []
media_N_2 = []
desv_pad_invasao = []
media_invasao = []
desv_pad_visita = []
media_visita = []
media_hist_N_2 = []
desv_pad_hist_N_2 = []


desv_pad_N_1, media_N_1 = calc_estatisticas(resultado1)
desv_pad_N_2, media_N_2 = calc_estatisticas(resultado2)
desv_pad_invasao, media_invasao = calc_estatisticas(resultado_invasao)
desv_pad_visita, media_visita = calc_estatisticas(resultado_visita)
desv_pad_hist_N_2, media_hist_N_2 = calc_estatisticas(resultado_N2)

avaliacao_anormal_N_1 = []
avaliacao_anormal_N_2 = []
avaliacao_anormal_invasao = []
avaliacao_anormal_visita = []

valores_anormais_faixa_N_1 = []
valores_anormais_faixa_N_2 = []
valores_anormais_faixa_invasao = []
valores_anormais_faixa_visita = []

valores_anormais_N_1 = []
valores_anormais_N_2 = []
valores_anormais_invasao = []
valores_anormais_visita = []

numero_alertas_N_1 = []
numero_alertas_N_2 = []
numero_alertas_invasao = []
numero_alertas_visita = []

log_alertas_N_1 = []
log_alertas_N_2 = []
log_alertas_invasao = []
log_alertas_visita = []

avaliacao_anormal_N_1,valores_anormais_faixa_N_1,valores_anormais_N_1,numero_alertas_N_1, log_alertas_N_1 = analisa_resultado(resultado1)
avaliacao_anormal_N_2,valores_anormais_faixa_N_2,valores_anormais_N_2,numero_alertas_N_2, log_alertas_N_2 = analisa_resultado(resultado2)
avaliacao_anormal_invasao,valores_anormais_faixa_invasao,valores_anormais_invasao,numero_alertas_invasao, log_alertas_invasao = analisa_resultado(resultado_invasao)
avaliacao_anormal_visita,valores_anormais_faixa_visita,valores_anormais_visita,numero_alertas_visita, log_alertas_visita = analisa_resultado(resultado_visita)




'''
prob_result1 = []
prob_result2 = []
for elemento in resultado1[1:]:
    prob_result1.append(elemento[3])
for elemento in resultado2[1:]:
    prob_result2.append(elemento[3])

desv_pad1 = np.std(prob_result1)
media1 = np.mean(prob_result1)
desv_pad2 = np.std(prob_result2)
media2 = np.mean(prob_result2)
'''
'''
avaliacao_anormais1 = []
avaliacao_anormais2 = []
avaliacao_anormais_invasao = []
avaliacao_anormais_visita = []
valores_anormais_faixa_N_1 = [["0 - 20", "21 - 40", "41 - 60", "61 - 80", "81+"],[0,0,0,0,0]]
valores_anormais_faixa_N_2 = [["0 - 20", "21 - 40", "41 - 60", "61 - 80", "81+"],[0,0,0,0,0]]
valores_anormais_faixa_invasao = [["0 - 20", "21 - 40", "41 - 60", "61 - 80", "81+"],[0,0,0,0,0]]
valores_anormais_faixa_visita = [["0 - 20", "21 - 40", "41 - 60", "61 - 80", "81+"],[0,0,0,0,0]]
#menor_prob = []
maior_valor_anormal1 = 0
valores_anormais1 = []
maior_valor_anormal2 = 0
valores_anormais2 = []
maior_valor_anormal_invasao = 0
valores_anormais_invasao = []
maior_valor_anormal_visita = 0
valores_anormais_visita = []
numero_alertas_N_1 = [0,0,0,0]
numero_alertas_N_2 = [0,0,0]
numero_alertas_invasao = [0,0,0]
numero_alertas_visita = [0,0,0]

for elemento in probabilidades_eventos:
    if elemento[-1] < 0.3:
        menor_prob.append(elemento)


for avaliacao in resultado1[1:]:
    if avaliacao[-1] == "SIM":
        avaliacao_anormais1.append(avaliacao)
    if avaliacao[-2] > maior_valor_anormal1:
        maior_valor_anormal1 = avaliacao[-2]
        valores_anormais1.append(avaliacao)
    if avaliacao[-2] <= 0.2:
        valores_anormais_faixa_N_1[1][0] += 1
    elif avaliacao[-2] > 0.2 and avaliacao[-2] <= 0.4:
        valores_anormais_faixa_N_1[1][1] += 1
    elif avaliacao[-2] > 0.4 and avaliacao[-2] <= 0.6:
        valores_anormais_faixa_N_1[1][2] += 1
    elif avaliacao[-2] > 0.6 and avaliacao[-2] <= 0.8:
        valores_anormais_faixa_N_1[1][3] += 1
    elif avaliacao[-2] > 0.8:
        valores_anormais_faixa_N_1[1][4] += 1

for avaliacao in resultado2[1:]:
    if avaliacao[-1] == "SIM":
        avaliacao_anormais2.append(avaliacao)
    if avaliacao[-2] > maior_valor_anormal2:
        maior_valor_anormal2 = avaliacao[-2]
        valores_anormais2.append(avaliacao)
    if avaliacao[-2] > 0.8 and avaliacao[-2] <= 0.89:
        numero_alertas[0] += 1
    elif avaliacao[-2] > 0.89 and avaliacao[-2] <= threshold:
        numero_alertas[1] += 1
    elif avaliacao[-2] > threshold:
        numero_alertas[2] += 1
    if avaliacao[-2] <= 0.2:
        valores_anormais_faixa_N_2[1][0] += 1
    elif avaliacao[-2] > 0.2 and avaliacao[-2] <= 0.4:
        valores_anormais_faixa_N_2[1][1] += 1
    elif avaliacao[-2] > 0.4 and avaliacao[-2] <= 0.6:
        valores_anormais_faixa_N_2[1][2] += 1
    elif avaliacao[-2] > 0.6 and avaliacao[-2] <= 0.8:
        valores_anormais_faixa_N_2[1][3] += 1
    elif avaliacao[-2] > 0.8:
        valores_anormais_faixa_N_2[1][4] += 1

for avaliacao in resultado_invasao[1:]:
    if avaliacao[-1] == "SIM":
        avaliacao_anormais_invasao.append(avaliacao)
    if avaliacao[-2] > maior_valor_anormal2:
        maior_valor_anormal_invasao = avaliacao[-2]
        valores_anormais_invasao.append(avaliacao)
    if avaliacao[-2] > 0.8 and avaliacao[-2] <= 0.89:
        numero_alertas[0] += 1
    elif avaliacao[-2] > 0.89 and avaliacao[-2] <= threshold:
        numero_alertas[1] += 1
    elif avaliacao[-2] > threshold:
        numero_alertas[2] += 1
    if avaliacao[-2] <= 0.2:
        valores_anormais_faixa_invasao[1][0] += 1
    elif avaliacao[-2] > 0.2 and avaliacao[-2] <= 0.4:
        valores_anormais_faixa_invasao[1][1] += 1
    elif avaliacao[-2] > 0.4 and avaliacao[-2] <= 0.6:
        valores_anormais_faixa_invasao[1][2] += 1
    elif avaliacao[-2] > 0.6 and avaliacao[-2] <= 0.8:
        valores_anormais_faixa_invasao[1][3] += 1
    elif avaliacao[-2] > 0.8:
        valores_anormais_faixa_invasao[1][4] += 1

for avaliacao in resultado_visita[1:]:
    if avaliacao[-1] == "SIM":
        avaliacao_anormais_visita.append(avaliacao)
    if avaliacao[-2] > maior_valor_anormal2:
        maior_valor_anormal_visita = avaliacao[-2]
        valores_anormais_visita.append(avaliacao)
    if avaliacao[-2] > 0.8 and avaliacao[-2] <= 0.89:
        numero_alertas[0] += 1
    elif avaliacao[-2] > 0.89 and avaliacao[-2] <= threshold:
        numero_alertas[1] += 1
    elif avaliacao[-2] > threshold:
        numero_alertas[2] += 1
    if avaliacao[-2] <= 0.2:
        valores_anormais_faixa_N_2[1][0] += 1
    elif avaliacao[-2] > 0.2 and avaliacao[-2] <= 0.4:
        valores_anormais_faixa_N_2[1][1] += 1
    elif avaliacao[-2] > 0.4 and avaliacao[-2] <= 0.6:
        valores_anormais_faixa_N_2[1][2] += 1
    elif avaliacao[-2] > 0.6 and avaliacao[-2] <= 0.8:
        valores_anormais_faixa_N_2[1][3] += 1
    elif avaliacao[-2] > 0.8:
        valores_anormais_faixa_N_2[1][4] += 1
'''
'''
vetor_teste = []
vetor_teste.append(vetor_verificacao[0])
dia = vetor_teste[0][0]
hora = vetor_teste[0][1]
data = vetor_teste[0][2]
vetor_teste.append([dia,hora,data,'pres_lavanderia','ON'])
vetor_teste.append([dia,hora,data,'luz_corredor','ON'])
vetor_teste.append([dia,hora,data,'pres_quarto3','ON'])
resultado,threshold_ocorrido, media, desv_pad = classificador2_0(start_end_vect, vetor_teste, lista_eventos)
'''
print("a")


'''


########################################## dados artigo ##########################################

#test = [[1,5,2,3,4],[1,3,4,3,5],[1,2,3,4],[1,3,5],[4,5]]
#a = AprioriAll(test,0.6,[1,2,3,4,5])

large1 = []
for i in range(max(max(matrix_dados))+1):
    large1.append(i)
eventos = AprioriAll(matrix_dados,0.45,large1)
        
 


eventos_sensor = []
for seq in eventos:
    for i in range(len(seq)):
        aux = []
        for indice_sensor in seq[i]:
            aux.append(sensores[int(indice_sensor)])
        eventos_sensor.append(aux)
aux = []
for dia in matrix_dados_aux:
    for elemento in dia:
        aux.append(elemento)
matrix_dados_aux = aux
aux = []
for elemento in eventos_sensor:
    for item in elemento:
        if not(item in aux):
            aux.append(item)
eventos_sensor = aux
start_end_vect = start_end_time(matrix_dados_aux, eventos_sensor)

relacoes = []
numero_ocorrencias = []
for elemento in start_end_vect:
    relacoes.append([elemento[0][1]])
    numero_ocorrencias.append(len(elemento))
for x in range(len(start_end_vect)):
    resultado = [] #contem as relacoes de um dado sensorX com todos os outros sensores da base
    for y in range(len(start_end_vect)):
        if x != y:
            #print("sensorX: ", start_end_vect[x][0][1])
            resultado.append(relacao_temporal(start_end_vect[x],start_end_vect[y]))
            #print(resultado[0])
            #print(resultado[1])
    relacoes[x].append(resultado)


probabilidades_eventos = probabilidade(relacoes,numero_ocorrencias) #contem a probabilidades dos eventos Y ocorrerem dado q ocorreu um evento X
valores_anormais = [] #valor de anormalidade de um evento Y dado que X ocorreu
valores_anormais_busca = []# vetor auxiliar para buscar o valor de anormalidade de Y
probabilidades_valores = []# vetor que contem apenas as probabilidades do vetor "probabilidades_eventos"



for elemento in probabilidades_eventos:
    valores_anormais.append([elemento[0],elemento[1],1-elemento[2]])
    valores_anormais_busca.append([eventos_sensor.index(elemento[0]),eventos_sensor.index(elemento[1])])
    probabilidades_valores.append(1 - elemento[2])
desv_pad = np.std(probabilidades_valores)
media = np.mean(probabilidades_valores)
threshold_ocorrido = media + 2 * desv_pad
if threshold_ocorrido > 1.0:
    threshold_ocorrido = 1.0 
for ind_ultimo_dia in range(len(dados)):
    if dados[ind_ultimo_dia][0] == ultimo_dia:
        break

vetor_verificacao = dados[ind_ultimo_dia:].copy()


eventos_ocorridos = []
indice = 0
classificacao = [["evento", "probabilidade do evento", "valor de anormalidade","detectada anomalia"]]
while True:
    sensor_avaliado = vetor_verificacao[indice][-2]
    if sensor_avaliado in eventos_sensor and sensor_avaliado not in eventos_ocorridos and vetor_verificacao[indice][-1] == "ON":
        eventos_ocorridos.append(sensor_avaliado)
    if len(eventos_ocorridos) == 2:
        evento_avaliado = eventos_ocorridos[-1]
        evento_ocorrido = eventos_ocorridos[-2]
        indice_anormalidade = busca_probabilidade(eventos_sensor.index(evento_avaliado),eventos_sensor.index(evento_ocorrido),valores_anormais_busca) # indice no qual se encontra a probabilidade buscada
        if valores_anormais[indice_anormalidade][2] >= threshold_ocorrido:
            classificacao.append([evento_avaliado,probabilidades_eventos[indice_anormalidade][2], valores_anormais[indice_anormalidade][2], "SIM"])
        else:
            classificacao.append([evento_avaliado,probabilidades_eventos[indice_anormalidade][2], valores_anormais[indice_anormalidade][2],"NAO"])
        break
    indice +=1
    if indice == len(vetor_verificacao):
        print("nao occoreram eventos frequentes")
        break

for i in range(indice, len(vetor_verificacao)):
    sensor_avaliado = vetor_verificacao[i][-2]
    if sensor_avaliado in eventos_sensor and sensor_avaliado != eventos_ocorridos[-1] and vetor_verificacao[indice][-1] == "ON":
        eventos_ocorridos.append(sensor_avaliado)
        evento_avaliado = eventos_ocorridos[-1]
        evento_ocorrido = eventos_ocorridos[-2]
        indice_anormalidade = busca_probabilidade(eventos_sensor.index(evento_avaliado),eventos_sensor.index(evento_ocorrido),valores_anormais_busca) # indice no qual se encontra a probabilidade buscada
        if valores_anormais[indice_anormalidade][2] >= threshold_ocorrido:
            classificacao.append([evento_avaliado,probabilidades_eventos[indice_anormalidade][2], valores_anormais[indice_anormalidade][2], "SIM"])
        else:
            classificacao.append([evento_avaliado,probabilidades_eventos[indice_anormalidade][2], valores_anormais[indice_anormalidade][2],"NAO"])
print("a")


"""
for sensor in start_end_vect:
    for elemento in sensor:
        for item in elemento:
            print(item, end= "       ")
        print(" ")
    print("\n\n\n")
print("a")
"""


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


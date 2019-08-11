import time
from datetime import datetime as dt
from datetime import timedelta
import datetime
import segmentacao

dados_casa = segmentacao.dados_casa
dados_acesso = segmentacao.dados_acesso
transicoes = segmentacao.transicoes
print("\n\n\n\n\n")
"""
entrada
vetor_sensor: vetor de dados contendo as informacoes brutas dos sensores da casa
comodo: indice que indica de qual comodo o vetor_sensor veio

esta funcao mapeia o estado de todos os comodos da casa 
"""
def maq_estados(vetor_sensor, comodo):
    pass
def rotula_base(vetor_sensor):
    pass

"""
entrada
vetor_sensor: vetor de dados contendo as informacoes brutas dos sensores da casa

classifica o segmento 
"""
def corredor(vetor_sensor):
    luz_corredor = 12
    pres_corredor = 22
    estado_aceso = 0
    estado_vazio = 0
    estado_transicao = 0
    estados = []
    segmentos = []
    segmento_atual = []

    for i in range(len(vetor)):
        if vetor_sensor[i][pres_corredor] >= 150 and vetor_sensor[i][luz_corredor] == 1: #Contador de presença >= tempo determinado e luz acesa
            estado_aceso += 1 #Determinar estado aceso
            estado_vazio = 0
            estado_transicao = 0

            if estado_aceso == 1:
                if len(segmento_atual) != 0:
                    segmentos.append(segmento_atual)
                segmento_atual = []
                estados.append("luz acesa")
            segmento_atual.append(vetor_sensor[i])
            
            if (i == len(vetor)-1):
                segmentos.append(segmento_atual)

        elif vetor_sensor[i][pres_corredor] >= 150 and vetor_sensor[i][luz_corredor] == 0: #Contador de presença >= tempo determinado e luz acesa
            estado_vazio += 1 #Determinar estado vazio
            estado_aceso = 0
            estado_transicao = 0

            if estado_vazio == 1:
                if len(segmento_atual) != 0:
                    segmentos.append(segmento_atual)
                segmento_atual = []
                estados.append("vazio")
            segmento_atual.append(vetor_sensor[i])

            if i == len(vetor)-1:
                segmentos.append(segmento_atual)

        elif vetor_sensor[i][pres_corredor] < 150:
            estado_transicao += 1 
            estado_aceso = 0
            estado_vazio = 0

            if estado_transicao == 1:
                if len(segmento_atual) != 0:
                    segmentos.append(segmento_atual)
                segmento_atual = []
                estados.append("transicao corredor")
            segmento_atual.append(vetor_sensor[i])
            
            if i == len(vetor)-1:
                segmentos.append(segmento_atual)
            

    return estados, segmentos

"""
entrada
vetor_sensor: vetor de dados contendo as informacoes brutas dos sensores da casa

funcao diz se o acesso trata-se de uma entrada de morador ou saida de morador
"""
def entrada_saida(vetor_sensor, hora_entrada):
    hora_acesso = dt.strptime(hora_entrada, '%Y/%m/%d, %H:%M:%S')
    indice = 0
    while True:
        hora_casa = dt.strptime(vetor_sensor[indice][1][1:-1], '%Y-%m-%d %H:%M')
        if hora_casa - hora_acesso >= timedelta(seconds = 0): #encontrou o horario imediatamente depois do acesso 
            break
        indice += 1
    pres_anterior = vetor_sensor[0][18]

    for i in range(1,indice):
        pres_atual = vetor_sensor[i][18]
        if pres_atual < pres_anterior or pres_atual < 50:
            saida = True
            break
        else:
            saida = False
        pres_anterior = pres_atual
    
    for i in range(indice, len(vetor_sensor)):
        pres_atual = vetor_sensor[i][18] 
        if pres_atual < pres_anterior or pres_atual < 50:
            entrada = True
            break
        else:
            entrada = False
        pres_anterior = pres_atual

    return entrada, saida
        

"""
colocar esta funcao na segmentacao

entradas
dados_casa: matrix de dados contendo as informacoes brutas dos sensores da casa
dados_acesso: matrix de dados contendo as informacoes de acesso da casa

funcao retorna o vetor que corresponde a uma faixa de horarios compativel com o timestamp do vetor
dados_acesso
"""
def match_acesso_casa(dados_casa, dados_acesso):
    indice_atual = int(len(dados_casa)/2) #indice inicial para a busca do horario correspondente no vetor dados_acesso
    hora_casa = dt.strptime(dados_casa[indice_atual][1][1:-1], '%Y-%m-%d %H:%M')
    hora_acesso = dt.strptime(dados_acesso[1], '%Y/%m/%d, %H:%M:%S')
    limite_inferior = 0 #limite inferior para a busca da faixa de horarios
    limite_superior = len(dados_casa) #limite superior para a busca da faixa de horarios
    #indice_passados = [indice_atual]
    while True:
        if abs(hora_casa - hora_acesso) < timedelta(minutes = 10):
            break 
        elif hora_casa - hora_acesso < timedelta(seconds = 0): #hora_acesso esta depois de hora_casa
            prox_indice = int((indice_atual + limite_superior)/2)
            limite_inferior = indice_atual
        elif hora_casa - hora_acesso > timedelta(seconds = 0): #hora_acesso esta antes de hora_casa
            prox_indice = int((indice_atual + limite_inferior)/2)
            limite_superior = indice_atual
        if prox_indice == indice_atual:
            print("não existe faixa horario correspondente nos dados da casa")
            indice_atual = None
            break
        
        indice_atual = prox_indice
        hora_casa = dt.strptime(dados_casa[indice_atual][1][1:-1], '%Y-%m-%d %H:%M')

    if indice_atual == None:
        return None

    indice_inicial = indice_atual #indice no qual esta a ultima linha do vetor de retorno
    indice_final = indice_atual #indice no qual esta o primeira linha do vetor de retorno
    
    while True:
        prox_indice = indice_inicial - 1
        hora_casa = dt.strptime(dados_casa[prox_indice][1][1:-1], '%Y-%m-%d %H:%M')
        if abs(hora_casa - hora_acesso) > timedelta(minutes = 10):
            break
        indice_inicial = prox_indice
    while True:
        prox_indice = indice_final + 1 
        hora_casa = dt.strptime(dados_casa[prox_indice][1][1:-1], '%Y-%m-%d %H:%M')
        if abs(hora_casa - hora_acesso) > timedelta(minutes = 10):
            break
        indice_final = prox_indice
    return dados_casa[indice_inicial:indice_final]
   
#print(match_acesso_casa(dados_casa,dados_acesso[30]))

for i in range(1,len(transicoes[10])-1):
    indice_inicial = transicoes[10][i]
    indice_final = transicoes[10][i+1]
    
    #if indice_inicial == 103:
    #    print("a")
    
    vetor = dados_casa[indice_inicial:indice_final]
    resultado, segmento = corredor(vetor)
    if len(resultado) != 1:
        print("Mudança de feature!") #Caso de erro ocorre quando são detectadas 2 ou mais atividades em um segmento (ex: mudança de luz dentro de um segmento presença)
        print(resultado)
        print(segmento)
        print("indice inicial: ", indice_inicial)
        print("indice final: ", indice_final)
        print("\n\n")
        #break

    else:
        print(resultado)
        print("indice inicial: ", indice_inicial)
        print("indice final: ", indice_final)
        print("\n\n")

for i in range(1,len(dados_acesso)):
    if match_acesso_casa(dados_casa, dados_acesso[i]) == None:
        print("nao existe para: ", dados_acesso[i])
    else: 
        vetor = match_acesso_casa(dados_casa,dados_acesso[i])
        entrada, saida = entrada_saida(vetor, dados_acesso[i][1])
        print("entrada: ",entrada,"   ","saida: ",saida, "  ", dados_acesso[i][1])
        """
        print("inicial: ", vetor[0][1])
        print("final: ", vetor[-1][1])
        print("acesso: ", dados_acesso[i][1])
        """
    print("\n\n\n\n")


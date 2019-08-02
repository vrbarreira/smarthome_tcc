import time
from datetime import datetime as dt
from datetime import timedelta
import datetime
import segmentacao

dados_casa = segmentacao.dados_casa
dados_acesso = segmentacao.dados_acesso
transicoes = segmentacao.transicoes
for elemento in transicoes:
    elemento.insert(1,1)
    elemento.append(-1)

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
    vetor_retorno = []
    for i in range(len(vetor)):
        if vetor_sensor[i][pres_corredor] >= 150 and luz_corredor[luz_corredor] == 1:
            vetor_retorno.append("luz acesa")
        elif vetor_sensor[i][pres_corredor] >= 150 and luz_corredor[luz_corredor] == 0:
            vetor_retorno.append("vazio")
        elif vetor_sensor[i][pres_corredor] < 150:
            vetor_retorno.append("transicao corredor")
    return vetor_retorno

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
    vetor = dados_casa[indice_inicial:indice_final]
    print(corredor(vetor))
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


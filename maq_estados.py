import time
from datetime import datetime as dt
from datetime import timedelta
import datetime
import segmentacao

dados_casa = segmentacao.dados_casa
dados_acesso = segmentacao.dados_acesso
transicoes = segmentacao.transicoes
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

funcao que diz se trata-se de uma entrada de morador ou saida de morador
"""


def entrada_saida(vetor_sensor):
       pass

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
    indice_passados = [indice_atual]
    while True:
        print (indice_atual)
        if abs(hora_casa - hora_acesso) < timedelta(minutes = 10):
            break 
        elif hora_casa - hora_acesso < timedelta(seconds = 0): #hora_acesso esta depois de hora_casa
            prox_indice = int((indice_atual + len(dados_casa))/2)
        elif hora_casa - hora_acesso > timedelta(seconds = 0): #hora_acesso esta antes de hora_casa
            prox_indice = int(indice_atual/2)
        if insercao_binaria(indice_passados, prox_indice):
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
        if abs(hora_casa - hora_acesso) < timedelta(minutes = 10):
            break
        indice_inicial = indice_inicial - 1
        hora_casa = dt.strptime(dados_casa[indice_inicial][1][1:-1], '%Y-%m-%d %H:%M')
    while True:
        if abs(hora_casa - hora_acesso) < timedelta(minutes = 10):
            break
        indice_final = indice_final + 1 
        hora_casa = dt.strptime(dados_casa[indice_final][1][1:-1], '%Y-%m-%d %H:%M')
    return dados_casa[indice_inicial:indice_final]


"""
insere elemento num vetor usando a metodologia de busca binaria e diz se o elemento ja existe
"""
def insercao_binaria(vetor, elemento):
    indice_atual = int(len(vetor)/2)
    if elemento < vetor[0]:
        vetor.insert(0,elemento)
        return False
    elif elemento > vetor[-1]:
        vetor.insert(len(vetor),elemento)
        return False
    elif len(vetor) == 2 and elemento > vetor[0] and elemento < vetor[-1]:
        vetor.insert(1,elemento)
        return False
    else:
        while True:
            if vetor[indice_atual] > elemento:
                if vetor[indice_atual-1] < elemento and elemento < vetor[indice_atual+1]:
                    elemento_repitido = False
                    vetor.insert(indice_atual,elemento)
                    break
                    

                elif vetor[indice_atual-1] == elemento or elemento == vetor[indice_atual+1]:
                    elemento_repitido = True
                    break
                indice_atual = int(indice_atual/2)
            else:
                if vetor[indice_atual-1] < elemento and elemento < vetor[indice_atual+1]:
                    elemento_repitido = False
                    vetor.insert(indice_atual, elemento)
                    break
                    
                elif vetor[indice_atual-1] == elemento or elemento == vetor[indice_atual+1]:
                    elemento_repitido = True
                    break
                indice_atual = int((indice_atual+ len(vetor))/2)
                    
        return elemento_repitido
    

print(match_acesso_casa(dados_casa, dados_acesso[30]))

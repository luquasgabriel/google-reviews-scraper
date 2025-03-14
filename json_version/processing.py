import json
import os
import re

from scraping import fazer_requisicao, gerar_url_requisicao
from utils import obter_nome_nota_texto, formatar_token_caesy, extrair_cod_estabelecimento, extrair_nome_estabelecimento


#Diretório de saída
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
PASTA_SAIDA = os.path.join(BASE_DIR, "extracted")  
os.makedirs(PASTA_SAIDA, exist_ok=True) 


'''
Manipula as URLs de estabelecimentos do Google Maps, extraindo o ID e o nome do estabelecimento para iniciar a extração de avaliações
'''
def processar_estabelecimento(url_original):
    id_estabelecimento = extrair_cod_estabelecimento(url_original)
    if not id_estabelecimento:
        print(f"ID do estabelecimento não encontrado para a URL: {url_original}")
        return

    nome_estabelecimento = extrair_nome_estabelecimento(url_original)
    nome_estabelecimento = re.sub(r'[^\w\s-]', '', nome_estabelecimento).replace(' ', '_') #Limpa o nome do estabelecimento, mantendo apenas letras, números, espaços e hífens
    print(f"Iniciando extração de avaliações para {nome_estabelecimento}...\n")
    processar_avaliacoes(id_estabelecimento, nome_estabelecimento)


'''
Processa as avaliações de um estabelecimento, salvando os resultados em um arquivo JSON
'''
def processar_avaliacoes(codigo_estabelecimento, nome_estabelecimento):
    id_estabelecimento = codigo_estabelecimento.split(":")[-1]  #Coleta o ID do estabelecimento do código no formato 0x88dd8028577b37eb:0x1fef488ed7755aa0
    arquivo_saida = os.path.join(PASTA_SAIDA, f"avaliacoes_{nome_estabelecimento}_{id_estabelecimento}.json")

    #Inicializa o arquivo com a estrutura básica
    with open(arquivo_saida, 'w', encoding='utf-8') as file:
        json.dump({"estabelecimento": nome_estabelecimento, "media": 0.0, "avaliacoes": []}, file, indent=2, ensure_ascii=False)

    total_avaliacoes = 0
    soma_notas = 0
    avaliacoes_totais = []  # Lista para armazenar todas as avaliações

    url_primeira_pagina = gerar_url_requisicao(codigo_estabelecimento)  # Gera a URL para requisitar a primeira página de avaliações

    while True:
        dados = fazer_requisicao(url_primeira_pagina)
        if not dados:
            break

        try:
            avaliacoes = dados[2]  #As avaliações estão agrupadas em uma única lista, com suas informações inseridas em listas internas
            avaliacoes_filtradas = []  # Armazena as avaliações extraídas como dicionário, com nome, nota e texto

            for avaliacao in avaliacoes:
                nome, nota, texto = obter_nome_nota_texto(avaliacao)  # Extrai nome, nota e texto da avaliação
                if nome and nota is not None:  # Os campos nome e nota são obrigatórios, mas não necessariamente haverá texto
                    avaliacoes_filtradas.append({"nome": nome, "nota": nota, "texto": texto})
                    total_avaliacoes += 1
                    soma_notas += nota

            # Acumula as avaliações extraídas
            avaliacoes_totais.extend(avaliacoes_filtradas)

        except IndexError:
            print("Estrutura inesperada na resposta da requisição")
            break

        try:
            token_caesy = formatar_token_caesy(dados[1]) if dados[1] else None
            if not token_caesy:
                break
            url_primeira_pagina = gerar_url_requisicao(codigo_estabelecimento, token_caesy)#Busca a próxima página de avaliações através do "token caesy"
        except (IndexError, TypeError):
            break #Se não tiver o token na resposta, encerra o while (não há mais páginas de avaliações)

    # Salva as avaliações e a média do restaurante no arquivo ao final de toda a extração
    with open(arquivo_saida, 'w', encoding='utf-8') as file:
        media = round(soma_notas / total_avaliacoes, 1) if total_avaliacoes else 0.0
        json.dump({"estabelecimento": nome_estabelecimento, "media": media, "avaliacoes": avaliacoes_totais}, file, indent=2, ensure_ascii=False)

    print(f"Extração concluída para {nome_estabelecimento}. Total de avaliações extraídas: {total_avaliacoes}. Média do estabelecimento: {media}\n")

import re

from db import salvar_dados_no_banco
from scraping import fazer_requisicao, gerar_url_requisicao
from utils import obter_nome_nota_texto, formatar_token_caesy, extrair_cod_estabelecimento, extrair_nome_estabelecimento


'''
Manipula as URLs de estabelecimentos do Google Maps, extraindo o ID e o nome do estabelecimento para iniciar a extração de avaliações
'''
def processar_estabelecimento(url_original):
    codigo_estabelecimento = extrair_cod_estabelecimento(url_original)
    if not codigo_estabelecimento:
        print(f"ID do estabelecimento não encontrado para a URL: {url_original}")
        return

    nome_estabelecimento = extrair_nome_estabelecimento(url_original)
    nome_estabelecimento = re.sub(r'[^\w\s-]', '', nome_estabelecimento).replace(' ', '_') #Limpa o nome do estabelecimento, mantendo apenas letras, números, espaços e hífens
    print(f"Iniciando extração de avaliações para {nome_estabelecimento}...\n")
    processar_avaliacoes(codigo_estabelecimento, nome_estabelecimento)


'''
Processa as avaliações de um estabelecimento, salvando os resultados no banco de dados
'''
def processar_avaliacoes(codigo_estabelecimento, nome_estabelecimento):
    id_estabelecimento = codigo_estabelecimento.split(":")[-1]  # Extrai o ID do estabelecimento

    total_avaliacoes = 0
    soma_notas = 0
    avaliacoes_coletadas = []  # Lista para armazenar todas as avaliações antes de salvar no banco

    url_pagina = gerar_url_requisicao(codigo_estabelecimento)  # Gera a URL inicial

    while True:
        dados = fazer_requisicao(url_pagina)
        if not dados:
            print("Erro na requisição")
            break

        try:
            avaliacoes = dados[2]  # Lista de avaliações
            for avaliacao in avaliacoes:
                nome, nota, texto = obter_nome_nota_texto(avaliacao)  # Extrai nome, nota e texto
                if nome and nota is not None:  # Os campos nome e nota são obrigatórios
                    avaliacoes_coletadas.append({"nome": nome, "nota": nota, "texto": texto})
                    total_avaliacoes += 1
                    soma_notas += nota

        except IndexError:
            print("Estrutura inesperada na resposta da requisição")
            break

        # Tenta obter o token para a próxima página
        try:
            token_caesy = formatar_token_caesy(dados[1]) if dados[1] else None
            if not token_caesy:
                break
            url_pagina = gerar_url_requisicao(codigo_estabelecimento, token_caesy)  # Nova URL da próxima página
        except (IndexError, TypeError):
            break  # Se não houver token, não há mais páginas para processar

    # Após coletar todas as avaliações, salva no banco de uma vez só
    if avaliacoes_coletadas:
        salvar_dados_no_banco(nome_estabelecimento, id_estabelecimento, avaliacoes_coletadas)
        print(f"Extração concluída para {nome_estabelecimento}. Total de avaliações extraídas: {total_avaliacoes}. Nota do estabelecimento: {round(soma_notas / total_avaliacoes, 1) if total_avaliacoes > 0 else 0:.1f}\n")


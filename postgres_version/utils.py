import re
import urllib.parse


'''
Identifica o nome do estabelecimento a partir do path da URL

'''
def extrair_nome_estabelecimento(url):
    parsed_url = urllib.parse.urlparse(url)
    path_parts = parsed_url.path.split('/')
    nome_estabelecimento = path_parts[3]
    return urllib.parse.unquote(nome_estabelecimento).replace("+", " ")


'''
Retorna o código do estabelecimento a partir da URL, incluindo seu ID em hexadecimal. Pega o código que vem após "1s" e antes de "!".
Ex:
Input: https://www.google.com/maps/place/McDonald's/@28.3488543,-81.6468656,13z/data=!4m6!3m5!1s0x88dd8028577b37eb:0x1fef488ed7755aa0!8m2!3d28.3488543!4d-81.5768278!16s%2Fg%2F1tjs5rm6?entry=ttu&g_ep=EgoyMDI1MDMxMS4wIKXMDSoASAFQAw%3D%3D

Output: 0x88dd8028577b37eb:0x1fef488ed7755aa0
'''
def extrair_cod_estabelecimento(url):
    match = re.search(r"1s([A-Za-z0-9:]+)", url)
    return match.group(1) if match else None


'''
Extraindo nome, nota e texto da avaliação, que possui a estrutura de listas aninhadas.
'''
def obter_nome_nota_texto(avaliacao):
    try:
        nome = avaliacao[0][1][4][5][0]
    except (IndexError, TypeError):
        nome = None

    try:
        nota = avaliacao[0][2][0][0]
    except (IndexError, TypeError):
        nota = None

    try:
        texto = avaliacao[0][2][15][0][0]
    except (IndexError, TypeError):
        texto = None

    return nome, nota, texto


'''
Codifica o "token caesy" para que ele possa ser utilizado na URL de requisição, trocando "==" por "%3D%3D".
'''
def formatar_token_caesy(token_caesy):
    return token_caesy.replace("==", "%3D%3D") if token_caesy else None

import json
import requests


'''
Monta a URL de requisição para extração de avaliações. Caso haja um "token caesy", ele é incluído na URL e este direciona para a próxima página de reviews.
'''
def gerar_url_requisicao(codigo_estabelecimento, token_caesy=None):
    url_base = "https://www.google.com/maps/rpc/listugcposts?authuser=0&hl=pt-BR&gl=br&pb=!1m6!1s"
    url = f"{url_base}{codigo_estabelecimento}!6m4!4m1!1e1!4m1!1e3!2m2!1i10!2s"
    if token_caesy:
        url += f"{token_caesy}"
    url += "!5m2!1sn2fOZ8u9II6e5OUPu8as2AU!7e81!8m9!2b1!3b1!5b1!7b1!12m4!1b1!2b1!4m1!1e1!11m0!13m1!1e2"
    return url


''''
Remove caracteres indesejados da URL passada e retorna um JSON em formato de listas em listas.
'''
def fazer_requisicao(url):
    response = requests.get(url)
    if response.status_code == 200:
        resposta_limpa = response.text.lstrip("')]}\'")
        try:
            return json.loads(resposta_limpa)
        except json.JSONDecodeError:
            return None
    return None

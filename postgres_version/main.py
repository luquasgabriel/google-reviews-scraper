from processing import processar_estabelecimento
import concurrent.futures

'''
Aceita múltiplas URLs de estabelecimentos do Google Maps e inicia a extração de avaliações. Trabalha de forma concorrente, utilizando ThreadPoolExecutor
'''
def principal():
    urls = []
    while True:
        url = input("Insira a URL do estabelecimento (ou pressione Enter para iniciar): ")
        if not url.strip():
            break
        urls.append(url)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(processar_estabelecimento, urls)

if __name__ == "__main__":
    principal()

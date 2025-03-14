import hashlib
import psycopg2

from env import *

# Variaveis de ambiente
def conectar_banco():
    return psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )


"""
Gera um hash único para a avaliação baseado em nome, nota e texto.
"""
def gerar_hash(avaliacao):
    texto = avaliacao['texto'] if avaliacao['texto'] is not None else ''
    texto_hash = f"{avaliacao['nome']}|{avaliacao['nota']}|{texto}"
    return hashlib.sha256(texto_hash.encode()).hexdigest() #cria um hash único (de 256 bits) aplicando o algoritmo SHA-256 e retornando o resultado como uma string hexadecimal.


def salvar_dados_no_banco(nome_estabelecimento, google_id, avaliacoes):
    print(f"Inserindo dados de {nome_estabelecimento} no banco...")

    '''
    Insere um novo estabelecimento na tabela "estabelecimento".
    Se o google_id já existir (conflito), não faz nada.
    RETURNING id retorna o id do estabelecimento inserido.'
    '''
    try:
        with conectar_banco() as conn:
            with conn.cursor() as cursor:

                cursor.execute(
                    "INSERT INTO estabelecimento (google_id, nome) VALUES (%s, %s) ON CONFLICT (google_id) DO NOTHING RETURNING id;",
                    (google_id, nome_estabelecimento)
                )

                # Le a proxima linha e puxa o id do estabelecimento
                estabelecimento_id = cursor.fetchone()

                # Caso o estabelecimento não tenha sido inserido (já existia), buscamos o id pelo google_id
                if not estabelecimento_id:
                    cursor.execute("SELECT id FROM estabelecimento WHERE google_id = %s;", (google_id,))
                    estabelecimento_id = cursor.fetchone()
                
                # Verificamos se conseguimos pegar o id do estabelecimento
                if estabelecimento_id:
                    estabelecimento_id = estabelecimento_id[0]# retorno em tupla. Pegamos o primeiro elemento
                else:
                    print("[ERRO] Falha ao obter ID do estabelecimento!")
                    return

                # Buscamos os hashes das avaliações já existentes no banco para este estabelecimento
                cursor.execute("SELECT hash FROM avaliacao WHERE estabelecimento_id = %s;", (estabelecimento_id,))
                hashes_no_banco = {row[0] for row in cursor.fetchall()}# Armazenamos os hashes em um conjunto

                novos_hashes = set()

                for avaliacao in avaliacoes:
                    hash_avaliacao = gerar_hash(avaliacao) # Geramos o hash de cada avaliacao recebida com base no nome, nota e texto
                    novos_hashes.add(hash_avaliacao)
                    
                    # Se o hash da avaliação não existir no banco, inserimos a avaliação
                    if hash_avaliacao not in hashes_no_banco:
                        cursor.execute(
                            "INSERT INTO avaliacao (usuario_nome, nota, texto, hash, estabelecimento_id) VALUES (%s, %s, %s, %s, %s);",
                            (avaliacao['nome'], avaliacao['nota'], avaliacao['texto'], hash_avaliacao, estabelecimento_id)
                        )

                # Calculamos os hashes removidos (avaliações que estavam no banco, mas não estão mais)
                hashes_removidos = hashes_no_banco - novos_hashes

                # Só executa o UPDATE se o banco já tiver avaliações( caso contrario, as avaliações seriam marcadas como removidas logo de início)
                if hashes_removidos:
                    cursor.execute(
                        "UPDATE avaliacao SET removido = TRUE WHERE hash = ANY(%s);",
                        (list(hashes_removidos),)
                    )

                conn.commit()
                print(f'Dados de {nome_estabelecimento} salvos com sucesso!')
    except Exception as e:
        print(f"[ERRO] Ocorreu um erro ao salvar dados no banco: {e}") 
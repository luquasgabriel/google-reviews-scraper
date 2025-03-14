# Google Reviews Scraper
Esta é uma ferramenta para extrair dados de reviews de estabelecimentos publicados no Google através de URL's do Google Maps.
São coletadas e armazenadas informações como: nome do avaliador, nota, o texto da avaliação e outros dados relevantes.
A aplicação oferece duas versões, que determinam o tipo de armazenamento das informações: uma com armazenamento em formato JSON e outra com banco de dados PostgreSQL. Ambas utilizam multithreading para otimizar a velocidade do processo de coleta e armazenamento dos dados.

# Instalação

1. Certifique-se de que o Python está instalado em sua máquina.
2. Baixe os arquivos da versão desejada do repositório.
3. Dentro do diretório do projeto, crie um ambiente virtual com o comando:
   ```
   python -m venv .venv
   ```
4. Ative o ambiente virtual:
   - No Windows:
     ```
     .\.venv\Scripts\activate
     ```
   - No Linux/macOS:
     ```
     source .venv/bin/activate
     ```
5. Instale as dependências do projeto com:
   ```
   pip install -r requirements.txt
   ```

# Coleta de URL

1. Pesquise o estabelecimento em [Google Maps](https://www.google.com/maps/).
2. Copie a URL do estabelecimento no formato correto, como o exemplo abaixo:
   - Exemplo de URL:
     ```
     https://www.google.com/maps/place/McDonald's/@28.3488543,-81.6468656,13z/data=!4m6!3m5!1s0x88dd8028577b37eb:0x1fef488ed7755aa0!8m2!3d28.3488543!4d-81.5768278!16s%2Fg%2F1tjs5rm6?entry=ttu&g_ep=EgoyMDI1MDMxMS4wIKXMDSoASAFQAw%3D%3D
     ```
   - Visualização da página:
     ![Exemplo 1](https://github.com/user-attachments/assets/9c29f9ae-86a0-4f75-af42-5772363b6e83)

3. Caso encontre uma lista de estabelecimentos ou um link em outro formato, selecione o estabelecimento desejado e compartilhe sua localização. Acesse o link encurtado gerado e na página carregada, copie o link no formato correto.
   - Visualização da página:
     ![Exemplo 2](https://github.com/user-attachments/assets/304fd709-bafa-4ddf-b6a1-276fca2fa09f)

# Execução - Versão PostgreSQL

1. Certifique-se de que o PostgreSQL esteja instalado em sua máquina.
2. Crie as tabelas no banco de dados utilizando os comandos presentes no arquivo sql_commands.txt.
3. No arquivo env.py, configure as informações do banco de dados que você criou.
4. Execute o arquivo main.py, insira as URLs dos estabelecimentos desejados e, ao terminar, pressione ENTER com o campo em branco.
5. Aguarde a extração e o salvamento dos dados no banco de dados.

# Execução - Versão JSON

1. Execute o arquivo main.py, insira as URL's desejadas e ao terminar, pressione ENTER com o campo em branco;
2. Aguarde a extração e salvamento dos dados. Um arquivo .JSON será gerado para cada estabelecimento na pasta "extracted" dentro do diretório.









from selenium import webdriver # Módulo de automação de navegadores. Ele pode nos ajudar a abrir um navegador automaticamente
from selenium.webdriver.common.by import By #Usaremos o Selenium abrir uma página web automaticamente e para clicar em um botão.
from bs4 import BeautifulSoup # Módulo famoso para analisar/separar texto como HTML e executar ações nele, como encontrar tags HTML específicas
import time # Biblioteca que fará nosso código aguardar por algum tempo para que a página web possa ser carregada corretamente antes de começarmos a coletar os dados.
import pandas as pd # Biblioteca para podermos exportar os dados que coletamos em um arquivo CSV
from selenium import webdriver
import os

# PROCURE A VERSÃO DO SEU CHROME ASSIM:
# Clique nos 3 pontinhos -> Configurações -> Sobre o Chrome -> veja a versão

# LINK PARA ACHAR O WEBDRIVER NA VERSÃO CERTA
# https://googlechromelabs.github.io/chrome-for-testing/#stable

# SELECIONE A URL DA VERSAO DO WEBDRIVER DO SEU CHROME, COPIE E COLE NO NAVEGADOR
# FAÇA O DOWNLOAD, EXTRAIA A PASTA NESTA PASTA

# Se trocar o ChromeDriver, atualize o endereço abaixo para o endereço do seu chromedriver do seu PC
# Ela ajudará o pc a achar o chrome driver dentro desta pasta, pois pega o endereço da pasta.
dir = os.getcwd() + '\chromedriver-win64\chromedriver.exe'

#acessando o chrome driver no endereço guardado na variável dir. 
service = webdriver.ChromeService(executable_path=dir)

# Atribuindo o webdriver na variavel driver
driver = webdriver.Chrome(service=service)

# URL dos Exoplanetas da NASA - Link do site que queremos abrir utilizando o webdriver
driver.get('https://exoplanets.nasa.gov/exoplanet-catalog/')

time.sleep(10)

# Lista (vetor) para salvarmos todos os detalhes dos planetas
planets_data = []

# Função para coletar os dados do site
def scrape():

    for i in range(1, 2): # Aula 128 - Irá percorrer 1 página do site
        #print(f'Coletando dados da pagina {i+1} ...') #Imprimindo na tela, o número da página atual
        while True:
            time.sleep(2)

        # Objeto BeautifulSoup - Passamos o primeiro argumento como fonte da página do navegador usando o atributo .page_source para obter o código da página HTML e 
        # html.parser como segundo argumento para extrair o conteúdo da página das tags HTML.
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Verifique o número da página    
            current_page_num = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value"))

            if current_page_num < i:
                driver.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif current_page_num > i:
                driver.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break

        # Loop para encontrar o elemento dentro das tags ul e li usando a variável ul_tags.
        # #método soup.find_all() - temos que mencionar a tag e seus atributos. Ele encontrará todas as tags ul com classe “exoplanet”.
        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):

            li_tags = ul_tag.find_all("li") # Dentro das tags <li> podemos obter os dados listados. Aqui encontraremos todas as tags <li> dentro da tag <ul>
            # Ao percorrer essas tags <li> e buscar os dados, cria-se uma lista temporária e, posteriormente, anexaremos essa lista à lista planet_data que criamos anteriormente
                
            # Análise, para termos certeza de que tratamos a primeira tag <li> diferentemente das outras.
            # Crie-se uma lista vazia chamada temp_list.
            temp_list = [] 

            # Obtenha o li_tags com index usando a função enumerate(): retorna o índice junto com o elemento
            for index, li_tag in enumerate(li_tags): # Usa-se o método enumerate() para obter a lista de índices e tags.

                if index == 0: #Se o índice for zero, estamos anexando o conteúdo da tag <a> à temp_list.
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else: # Caso contrário: anexaremos o conteúdo de todas as tags <li>
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("") # Mas estamos tratando uma exceção, Se não houver nenhum conteúdo, anexe uma string vazia.

            # Aula 128: Obtenha a Tag do Hiperlink
            hyperlink_li_tag = li_tags[0]

            # Aula 128: Como temos que fornecer a URL completa, passe-se o site completo ao hiperlink
            temp_list.append("https://exoplanets.nasa.gov"+ hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            
            # Aula 128: Anexe o link agora completo em planets_data
            planets_data.append(temp_list) # E por ultimo, vamos anexar esta temp_list à planet_data.

            # Função find_element (encontrar elemento) - Para o navegador encontrar o botão
            # Ao encontrar o botão na página e clique para passar para a próxima página - Precisamos do XPath para localizá-lo
        driver.find_element(by=By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        # Aula 128 - Imprimindo o número da página atual que terminamos de coletar
        print(f"Coleta de dados da pagina {i} concluida")


# Chamando a função scrape() para coletar os dados do site
scrape()

# Precisamos armarzenar os dados em um arquivo CSV e assim, cria-se o cabeçalho com os nomes de coluna no arquivo CSV
# Desafio 01: Add na última posição, o cabeçalho para o hiperlink
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date"]

# Desafio 02: Defina planet_df_1 do pandas, para anexar a lista planets_data com os cabeçalhos das colunas.


# Desafio 03: Converta para CSV - método to_csv do pandas converte o dataframe em um arquivo csv - (passar nome_arquivo, add primeira coluna com nros série: atributo index, etiqueta "id")

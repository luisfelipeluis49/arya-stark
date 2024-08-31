from googlesearch import search
import requests
from bs4 import BeautifulSoup
import re

def extrair_data(soup):
    # Tentativa de encontrar data em meta tags comuns
    date_meta_tags = [
        ('meta', {'name': 'date'}),
        ('meta', {'property': 'article:published_time'}),
        ('meta', {'name': 'pubdate'}),
        ('meta', {'property': 'og:published_time'}),
    ]

    # Busca em meta tags
    for tag, attrs in date_meta_tags:
        meta = soup.find(tag, attrs=attrs)
        if meta and meta.get('content'):
            return meta['content']

    # Busca em tags <time>
    time_tag = soup.find('time')
    if time_tag and time_tag.get('datetime'):
        return time_tag['datetime']

    # Busca padrões de data no texto visível (exemplo: 2024-08-31)
    texto_visivel = ' '.join(soup.stripped_strings)
    padrao_data = re.search(r'\b\d{4}[-/]\d{2}[-/]\d{2}\b', texto_visivel)
    if padrao_data:
        return padrao_data.group()

    return "Data não encontrada"

def pesquisar_e_extrair_info(termo_pesquisa, num_resultados=5):
    # Adiciona 'news' à query para focar em notícias
    query = f"{termo_pesquisa} news"
    print(f"Realizando a busca na aba de notícias com a query: {query}")
    
    # Realiza a busca e coleta os resultados
    resultados = list(search(query, num_results=num_resultados))

    # Inicializa uma string vazia para armazenar todos os textos
    texto_final = ""

    if resultados:
        print("\nResultados encontrados:")
        for i, resultado in enumerate(resultados, start=1):
            print(f"{i}. {resultado}")

            # Tenta acessar e extrair informações da página
            try:
                response = requests.get(resultado)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extrai o título da página
                titulo = soup.title.string if soup.title else "Título não encontrado"
                # Extrai a data da página
                data = extrair_data(soup)
                # Extrai o conteúdo da página (primeiros 1000 caracteres)
                conteudo = ' '.join([p.get_text() for p in soup.find_all('p')])[:1000]

                # Adiciona as informações ao texto final
                texto_final += f"Título da Página: {titulo}\n"
                texto_final += f"Data da Página: {data}\n"
                texto_final += f"Conteúdo da Página: {conteudo}\n\n"

            except Exception as e:
                print(f"Erro ao tentar acessar {resultado}: {e}")
    else:
        texto_final = "Nenhum resultado encontrado."

    # Retorna o texto final com todas as informações
    return texto_final

# Exemplo de uso
termo = "alexandre de moraes"
texto_completo = pesquisar_e_extrair_info(termo)
print(texto_completo)
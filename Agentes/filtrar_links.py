import requests
from urllib.parse import urlparse

def google_search(query, cx, api_key, num_results=50):
    # Define a URL da API com os parâmetros ajustados para buscar mais resultados
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={query}&num={num_results}"
    response = requests.get(url)
    data = response.json()

    print(data)
    
    # Lista ampliada de domínios confiáveis
    trusted_domains = [
        # Jornais e revistas internacionais
        "bbc.com", "cnn.com", "nytimes.com", "reuters.com", "forbes.com", 
        "theguardian.com", "wsj.com", "bloomberg.com", "ft.com", "washingtonpost.com",
        "cnbc.com", "nbcnews.com", "aljazeera.com", "apnews.com", "economist.com",
        "time.com", "newsweek.com", "usatoday.com", "latimes.com", "businessinsider.com",
        "independent.co.uk", "telegraph.co.uk", "mirror.co.uk", "dailymail.co.uk",
        "elpais.com", "lemonde.fr", "spiegel.de", "corriere.it", "japantimes.co.jp",
        "scmp.com", "straitstimes.com",

        # Revistas e sites de negócios
        "wired.com", "techcrunch.com", "theverge.com", "arstechnica.com", "engadget.com",
        "gizmodo.com", "venturebeat.com", "cnet.com", "zdnet.com", "slashdot.org",
        "fastcompany.com", "inc.com", "hbr.org", "fortune.com", "qz.com", "seekingalpha.com",

        # Fontes brasileiras
        "globo.com", "uol.com.br", "folha.uol.com.br", "estadao.com.br", "gazetadopovo.com.br",
        "veja.abril.com.br", "exame.com", "valor.globo.com", "jovempan.com.br",
        "tecmundo.com.br", "canaltech.com.br", "olhardigital.com.br", "g1.globo.com",
        "infomoney.com.br", "epocanegocios.globo.com", "istoedinheiro.com.br",

        # Sites de tecnologia e inovação
        "recode.net", "macrumors.com", "9to5mac.com", "tomshardware.com", "pcmag.com",
        "androidcentral.com", "androidauthority.com", "bgr.com", "digitaltrends.com", "liliputing.com",
        "thenextweb.com", "mit.edu", "technologyreview.com", "futurism.com", "techspot.com",
        "producthunt.com", "hackaday.com", "howtogeek.com", "techrepublic.com", "itpro.co.uk"
    ]

    # Função auxiliar para extrair o domínio principal de uma URL
    def extract_domain(url):
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        return domain.replace('www.', '')

    # Exibir todos os links retornados pela API antes da filtragem
    if 'items' in data:
        print("Links retornados pela API (antes da filtragem):")
        for item in data['items']:
            print(item['link'])
    
    # Filtrar links relevantes com base nos domínios confiáveis
    filtered_results = []
    if 'items' in data:
        for item in data['items']:
            link = item.get('link', '')
            domain = extract_domain(link)
            # Verifica se o domínio principal está na lista de domínios confiáveis
            if any(trusted_domain in domain for trusted_domain in trusted_domains):
                filtered_results.append(item)

    # Exibir os links filtrados
    if filtered_results:
        print("\nLinks filtrados:")
        for result in filtered_results:
            print(f"Título: {result['title']}")
            print(f"Link: {result['link']}\n")
    else:
        print("\nNenhum link relevante encontrado após a filtragem.")

    return filtered_results

# Parâmetros de exemplo (insira suas credenciais)
api_key = ""  # Substitua pela sua chave de API
cx = ""  # Substitua pelo seu ID de mecanismo de pesquisa personalizado
query = "Microsoft"

# Chama a função de pesquisa com filtros
google_search(query, cx, api_key)

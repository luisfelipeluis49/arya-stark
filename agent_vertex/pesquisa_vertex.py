import base64
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import re

def generate(texto_completo):
    vertexai.init(project="arya-hackathon", location="us-central1")
    model = GenerativeModel(
        "gemini-1.5-flash-001",
        system_instruction=["""Você é um assistente especializado em resumir e avaliar pesquisas de notícias. Sua tarefa é analisar o título, data de publicação e o corpo do texto das páginas coletadas, avaliar se as fontes são confiáveis (especificamente jornais e revistas), e gerar um relatório estruturado com as seguintes seções:

        **1. Fontes confiáveis:**
        - Forneça linha por linha as fontes que você considerou confiáveis.

        **2. Resumo:**
        - Forneça um resumo conciso que destaque as principais informações das notícias encontradas, combinando o conteúdo de forma clara e objetiva.

        **3. Avaliação:**
        - Atribua uma nota de 1 a 5 com base na presença de conteúdos verdadeiramente sensíveis que possam comprometer a imagem da pessoa ou empresa relacionada. Utilize as seguintes diretrizes para a avaliação:
        - **Fraude e Corrupção:** Considere a presença de notícias que mencionem fraudes, corrupção, lavagem de dinheiro ou outras atividades ilegais. Notas mais baixas devem ser atribuídas se essas práticas forem identificadas.
        - **Sonegação e Irregularidades Fiscais:** Avalie a presença de informações sobre sonegação de impostos, evasão fiscal ou outras irregularidades financeiras. Se houver indícios significativos, reduza a nota.
        - **Processos Legais e Litígios:** Inclua processos judiciais em andamento ou concluídos, especialmente os que envolvem práticas antiéticas, má conduta empresarial, ou disputas trabalhistas.
        - **Controvérsias Públicas:** Considere notícias que indiquem controvérsias públicas, como declarações polêmicas, envolvimento em escândalos, comportamento antiético de executivos, ou má reputação pública.
        - **Impacto Ambiental e Social Negativo:** Leve em conta notícias sobre impactos ambientais, práticas prejudiciais à sociedade, ou falhas de conformidade com regulamentações ESG (ambiental, social, governança).
        - **Problemas Técnicos e Operacionais:** Não considere falhas técnicas, erros operacionais comuns, ou controvérsias menores que não comprometam substancialmente a reputação da empresa. Exemplos incluem falhas de software, atrasos em lançamentos, ou problemas que são corrigidos de forma proativa pela empresa.
        - **Posicionamento da Empresa/Pessoa:** Avalie se a empresa ou pessoa apresentou posicionamentos defensivos ou corretivos que possam influenciar positivamente a nota, especialmente em relação a questões críticas.

        **Critérios de Avaliação da Nota:**
        - **Nota 1:** Múltiplos conteúdos altamente sensíveis, incluindo fraudes, sonegação e outros delitos graves.
        - **Nota 2:** Histórico considerável de conteúdos sensíveis que podem prejudicar a imagem.
        - **Nota 3:** Presença moderada de conteúdos sensíveis, mas com algum esforço corretivo ou de defesa. Questões técnicas menores não devem impactar significativamente.
        - **Nota 4:** Pequenas controvérsias ou eventos isolados sem grande impacto negativo. Problemas técnicos que foram resolvidos ou que são comuns em qualquer empresa devem ser vistos como normais.
        - **Nota 5:** Não há conteúdos sensíveis significativos; a imagem da empresa/pessoa é sólida.

        **4. Justificativa:**
        - Explique brevemente a razão da nota atribuída, referindo-se aos conteúdos encontrados e destacando os fatores mais relevantes que influenciaram a avaliação. Problemas menores, como falhas técnicas, devem ser contextualizados como normais e sem grande impacto.

        **5. Referências:**
        - Liste 2 a 3 links das páginas analisadas que serviram de base para a justificativa e avaliação.

        Lembre-se de focar nas principais informações de cada artigo e evitar redundâncias. O objetivo é fornecer um resumo claro, uma avaliação justa baseada nas diretrizes fornecidas, e uma justificativa bem fundamentada. Garanta que problemas menores não afetem desproporcionalmente a nota final da avaliação."""] 

    )
    responses = model.generate_content(
        [f"{texto_completo}"],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    for response in responses:
        print(response.text, end="")

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

def pesquisar_e_extrair_info(termo_pesquisa, num_resultados=30):
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
                # Define um timeout de 5 segundos
                response = requests.get(resultado, timeout=5)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extrai o título da página
                titulo = soup.title.string if soup.title else "Título não encontrado"
                # Extrai a data da página
                data = extrair_data(soup)
                # Extrai o conteúdo da página (primeiros 1000 caracteres)
                conteudo = ' '.join([p.get_text() for p in soup.find_all('p')])[:10000]

                # Adiciona as informações ao texto final, incluindo o link
                texto_final += f"Título da Página: {titulo}\n"
                texto_final += f"Link: {resultado}\n"
                texto_final += f"Data da Página: {data}\n"
                texto_final += f"Conteúdo da Página: {conteudo}\n\n"

            except requests.exceptions.Timeout:
                print(f"Timeout ao tentar acessar {resultado}. Pulando para o próximo link.")
            except Exception as e:
                print(f"Erro ao tentar acessar {resultado}: {e}")
    else:
        texto_final = "Nenhum resultado encontrado."

    # Retorna o texto final com todas as informações
    return texto_final

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
]

# Exemplo de uso
termo = "Oracle"

texto_completo = pesquisar_e_extrair_info(termo)
generate(texto_completo)

import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting
import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Credenciais da API do Google
api_key = ""  # Substitua pela sua chave de API
cx = ""  # Substitua pelo seu ID de mecanismo de pesquisa personalizado

def main_agent(nome_empresa, politicas):
    # Define as funções e seus respectivos argumentos
    agentes = [
        (agente_risco_financeiro, (nome_empresa, politicas)),
        (agente_risco_operacional, (nome_empresa, politicas)),
        (agente_risco_legal_regulatorio, (nome_empresa, politicas)),
        (agente_risco_reputacao, (nome_empresa, politicas)),
        (agente_risco_mercado, (nome_empresa, politicas)),
        (agente_risco_tecnologico, (nome_empresa, politicas)),
        (agente_risco_ambiental_social, (nome_empresa, politicas))
    ]

    # Lista para armazenar os resultados
    resultados = []

    # Executa as funções em paralelo utilizando ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        # Mapeia as funções para o executor e inicia a execução
        futuros = {executor.submit(func, *arg): func.__name__ for func, arg in agentes}

        # Coleta os resultados conforme as tarefas são concluídas
        for futuro in as_completed(futuros):
            funcao_nome = futuros[futuro]
            try:
                resultado = futuro.result()
                resultados.append((funcao_nome, resultado))
            except Exception as e:
                resultados.append((funcao_nome, f"Erro ao executar {funcao_nome}: {e}"))

    # Imprime os resultados após todas as threads terem sido concluídas
    for funcao_nome, resultado in resultados:
        print(f"\n### Resultado da {funcao_nome} ###")
        print(resultado)

    # Retorna todos os resultados
    return resultados

# Função para gerar um resumo de um site específico
def agente_resumo_site(texto_completo, tipo_risco):
    vertexai.init(project="arya-hackathon", location="us-central1")
    model = GenerativeModel(
        "gemini-1.5-flash-001",
        system_instruction=[f"""Você é um assistente especializado em {tipo_risco}. Sua tarefa é analisar o conteúdo coletado de uma única fonte e gerar um resumo realmente conciso focado em possiveis gafes.
        **Resumo:** Forneça um resumo das informações coletadas da página individual.
        """]
    )
    responses = model.generate_content(
        [f"{texto_completo}"],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    resultado = ""
    for response in responses:
        resultado += response.text

    return resultado

def google_search(query, cx, api_key, num_results=5):
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={query}&num={num_results}"
    response = requests.get(url)
    data = response.json()
    return data['items']

def extract_text_from_url(url, max_chars=1000):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se a requisição foi bem sucedida

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extrair título da página
        title = soup.title.string if soup.title else "Título não encontrado"

        # Remove scripts e estilos para capturar somente o texto relevante
        for script in soup(["script", "style"]):
            script.extract()

        # Extrair texto principal e limitar o número de caracteres
        text = soup.get_text(strip=True, separator=' ')
        text = text[:max_chars]  # Limita o texto ao máximo de caracteres especificado

        # Tenta encontrar a data de publicação, se não encontrar define como data atual
        date_published = soup.find('meta', property='article:published_time') or \
                         soup.find('meta', property='og:article:published_time')
        if date_published:
            date_published = date_published.get('content')[:10]  # Formata data como YYYY-MM-DD
        else:
            date_published = datetime.now().strftime('%Y-%m-%d')

        return {
            'title': title,
            'text': text,
            'date_published': date_published,
            'link': url
        }
    except requests.exceptions.RequestException as e:
        return None
    
# Função que executa as pesquisas e faz a análise com o Gemini
def executar_pesquisas(termos, tipo_risco, politicas):
    resumos = []  # Lista para armazenar os resumos de cada site

    for termo in termos:
        # Realiza a pesquisa no Google
        search_results = google_search(termo, cx, api_key)

        # Extrai informações dos resultados
        for result in search_results:
            extracted_data = extract_text_from_url(result['link'])
            if extracted_data:
                # Formata os dados extraídos na estrutura desejada
                texto_completo = (
                    f"Link: {result['link']}\n"
                    f"Título: {extracted_data['title']}\n"
                    f"Data: {extracted_data['date_published']}\n"
                    f"Conteúdo: {extracted_data['text']}\n"
                )
                #print(texto_completo)  # Para debug, pode ser removido depois

                # Envia o resumo formatado para o Gemini
                resumo = agente_resumo_site(texto_completo, tipo_risco)
                resumos.append(resumo)

    # Junta os resumos em um único texto para a análise final
    texto_resumos = "\n".join(resumos)
    avaliacao = agente_analise_resumos(texto_resumos, tipo_risco, politicas)
    return avaliacao

# Função para análise final dos resumos gerados
def agente_analise_resumos(texto_resumos, tipo_risco, politicas):
    vertexai.init(project="arya-hackathon", location="us-central1")
    model = GenerativeModel(
        "gemini-1.5-flash-001",
        system_instruction = [f"""
        Você é um assistente especializado em análise de {tipo_risco} para um prestador de serviços bancários, principalmente para transações (PIX e TED) e fornecimento de crédito. Sua tarefa é analisar os resumos coletados de várias fontes online sobre uma empresa e avaliar o impacto e a probabilidade de riscos financeiros se materializarem nos próximos tempos para a empresa que fornecerá os serviços.

        **Contexto de Avaliação:**
        1. Considere não apenas os problemas específicos mencionados nos resumos, mas também o tamanho, a estrutura, a solidez financeira e a reputação da empresa no mercado. Empresas bem estabelecidas e com histórico sólido podem suportar problemas técnicos ou pequenos incidentes sem comprometer sua estabilidade.
        2. Para empresas grandes e bem estruturadas, avalie se os problemas apresentados têm relevância significativa ou se são aspectos pontuais que não afetam sua operação de forma crítica.
        3. Para empresas menores ou menos estáveis, mesmo pequenos problemas podem ter impactos mais severos. Ajuste sua avaliação conforme a resiliência e a capacidade da empresa de gerenciar esses riscos.
        4. Utilize seu conhecimento prévio sobre o setor, o histórico da empresa e suas capacidades de gestão de crise para contextualizar a gravidade dos riscos mencionados.

        **Critérios de Avaliação:**
        - Atribua uma nota de 1 a 5 para o impacto, considerando o efeito potencial do risco sobre a estabilidade financeira e operacional da empresa.
        - Atribua uma nota de 1 a 5 para a probabilidade, levando em conta a frequência com que esses problemas ocorrem e a capacidade da empresa de mitigá-los.

        - Note que pequenas falhas técnicas, ou incidentes que não afetam diretamente a reputação ou operações críticas de empresas robustas, devem ter impacto reduzido, enquanto problemas graves ou recorrentes em empresas menores devem ter impacto e probabilidade maiores.

        **Políticas da empresa**
        -Aqui está uma breve descrição das políticas da empresa que devem ser levadas em consideração para avaliar: {politicas}
        -Se a empresa estiver de acordo com as políticas da empresa, deve ser aliviada a análise.

        Utilize exatamente a estrutura descrita a seguir, só quero três informações, resumo geral, avaliação e justificativa, somente uma avaliação geral, sem avaliar diferentes aspectos.

        **Estrutura da Resposta:**
        1. **Resumo Geral:** Forneça um resumo geral conciso das informações coletadas, destacando os pontos principais.
        2. **Avaliação:** Atribua notas de 1 a 5 para impacto e probabilidade, com o formato: Impacto: 'valor', Probabilidade: 'valor' para o contexto geral em relação ao tipo de risco que estamos avaliando.
        3. **Justificativa:** Explique a razão das notas atribuídas, levando em consideração a relevância dos riscos para a empresa, sua estrutura, histórico, e o contexto do mercado. Destaque se os problemas são realmente críticos para a empresa em questão ou se são aspectos secundários que não comprometem sua operação de forma significativa.
        """]
    )
    responses = model.generate_content(
        [f"{texto_resumos}"],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    resultado = ""
    for response in responses:
        resultado += response.text

    return resultado

def extrair_data(soup):
    date_meta_tags = [
        ('meta', {'name': 'date'}),
        ('meta', {'property': 'article:published_time'}),
        ('meta', {'name': 'pubdate'}),
        ('meta', {'property': 'og:published_time'}),
    ]

    for tag, attrs in date_meta_tags:
        meta = soup.find(tag, attrs=attrs)
        if meta and meta.get('content'):
            return meta['content']

    time_tag = soup.find('time')
    if time_tag and time_tag.get('datetime'):
        return time_tag['datetime']

    texto_visivel = ' '.join(soup.stripped_strings)
    padrao_data = re.search(r'\b\d{4}[-/]\d{2}[-/]\d{2}\b', texto_visivel)
    if padrao_data:
        return padrao_data.group()

    return "Data não encontrada"

# Ajuste das funções para incluir termos mais neutros e informativos

def agente_risco_financeiro(nome_empresa, politicas):
    termos_risco_financeiro = [
        f"relatório financeiro {nome_empresa}",
        f"resultados financeiros {nome_empresa}",
        f"balanço financeiro {nome_empresa}",
        f"indicadores financeiros {nome_empresa}"
    ]
    resultado = executar_pesquisas(termos_risco_financeiro, "Risco Financeiro", politicas)
    print('agente risco financeiro concluído')
    return resultado

def agente_risco_operacional(nome_empresa, politicas):
    termos_risco_operacional = [
        f"operações {nome_empresa}",
        f"eficiência operacional {nome_empresa}",
        f"gestão e operações {nome_empresa}",
        f"processos internos {nome_empresa}"
    ]
    resultado = executar_pesquisas(termos_risco_operacional, "Risco Operacional", politicas)
    print('agente risco operacional concluído')
    return resultado

def agente_risco_legal_regulatorio(nome_empresa, politicas):
    termos_risco_legal = [
        f"conformidade regulatória {nome_empresa}",
        f"avaliação legal {nome_empresa}",
        f"regulamentação e {nome_empresa}",
        f"boas práticas regulatórias {nome_empresa}"
    ]
    resultado = executar_pesquisas(termos_risco_legal, "Risco Legal e Regulatório", politicas)
    print('agente risco legal regulatório concluído')
    return resultado

def agente_risco_reputacao(nome_empresa, politicas):
    termos_risco_reputacao = [
        f"imagem da {nome_empresa} na mídia",
        f"avaliação da reputação {nome_empresa}",
        f"percepção de marca {nome_empresa}",
        f"reconhecimento de marca {nome_empresa}"
    ]
    resultado = executar_pesquisas(termos_risco_reputacao, "Risco de Reputação", politicas)
    print('agente risco reputação concluído')
    return resultado

def agente_risco_mercado(nome_empresa, politicas):
    termos_risco_mercado = [
        f"posicionamento de mercado {nome_empresa}",
        f"estratégia de mercado {nome_empresa}",
        f"análise de mercado {nome_empresa}",
        f"crescimento de mercado {nome_empresa}"
    ]
    resultado = executar_pesquisas(termos_risco_mercado, "Risco de Mercado", politicas)
    print('agente risco mercado concluído')
    return resultado

def agente_risco_tecnologico(nome_empresa, politicas):
    termos_risco_tecnologico = [
        f"tecnologias da {nome_empresa}",
        f"inovação tecnológica {nome_empresa}",
        f"pesquisa e desenvolvimento {nome_empresa}",
        f"segurança da informação {nome_empresa}"
    ]
    resultado = executar_pesquisas(termos_risco_tecnologico, "Risco Tecnológico", politicas)
    print('agente risco tecnológico concluído')
    return resultado

def agente_risco_ambiental_social(nome_empresa, politicas):
    termos_risco_ambiental = [
        f"responsabilidade social {nome_empresa}",
        f"sustentabilidade {nome_empresa}",
        f"projetos sociais {nome_empresa}",
        f"estratégias ambientais {nome_empresa}"
    ]
    resultado = executar_pesquisas(termos_risco_ambiental, "Risco Ambiental e Social", politicas)
    print('agente risco ambiental e social concluído')
    return resultado

# Configurações do Gemini
generation_config = {
    "max_output_tokens": 8000,
    "temperature": 0.2,
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



# Exemplo de uso, aqui você pode chamar a função principal com o nome da empresa e as políticas da empresa, por exemplo:
# main_agent('Amazon', 'Nós temos foco em grandes empresas com potencial de inovação')
# main_agent('Google', 'Gosta de empresas com foco em sustentabilidade\nQueremos empresas que valorizem a diversidade')
# main_agent('Apple', 'Buscamos empresas com foco em inovação e design') 

empresa = 'Amazon' # Substitua pelo nome da empresa que deseja analisar
politicas = 'Nós temos foco em grandes empresas com potencial de inovação' # Substitua pelas políticas da empresa
main_agent(empresa, politicas)

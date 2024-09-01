# main.py - Arquivo para a API FastAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from requests import get
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting
import uvicorn

app = FastAPI()

# Configuração do projeto Vertex AI
PROJECT_ID = "arya-hackathon"
LOCATION = "us-central1"
MODEL_NAME = "gemini-1.5-flash-001"

# Configuração do modelo e safety settings
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 0.2,
    "top_p": 0.95,
}

cached_policies = None

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
    )
]

def getPolicies():
    if cached_policies is None:
        cached_policies = vertexai.get_policies()
    
    return cached_policies

# Função para gerar a análise
def generate_analysis(cnpj_input: str):
    getPolicies()
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = GenerativeModel(MODEL_NAME, project=PROJECT_ID, location=LOCATION, system_instruction=
                            ("Com base no JSON de análise do cliente (consultas de APIs de dados externos, politcas de KYC da StarkBank):(), você precisará se"))

    # Prompt com o CNPJ inputado
    text1 = f"""
    Você é um assistente de análise de risco especializado em avaliar empresas com base em dados financeiros, de crédito e de conformidade regulatória. 
    O cliente que estamos avaliando possui o CNPJ: {cnpj_input}.

    Com base nos dados coletados, faça uma análise completa sobre o risco de crédito deste cliente para o Stark Bank, considerando o contexto atual:

    - Informações Cadastrais: Razão social, atividade econômica (CNAE), situação cadastral, composição societária, e tempo de mercado.
    - Saúde Financeira: Balanço patrimonial, demonstração de resultados, fluxo de caixa, endividamento, score de crédito e histórico de pagamentos.
    - Compliance: Presença em listas de sanções ou registros de atividades irregulares.
    - Comportamento de Transações: Padrões de movimentação financeira, frequência e valores transacionados.

    Com base nesses dados, responda:
    1. Qual é a classificação de risco deste cliente?
    2. Quais são os principais pontos de atenção em relação ao risco financeiro e operacional?
    3. Quais recomendações você faria para o Stark Bank em relação a esta empresa?

    Considere todos os dados fornecidos e seja específico em sua análise, identificando oportunidades e riscos potenciais para o banco.
    """

    # Realiza a chamada para o modelo
    response = model.generate_content(
        [text1],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=False,
    )

    # Acessa o texto gerado corretamente
    result_text = response.text  # Corrigido para acessar o texto da resposta diretamente

    # Retorna o texto gerado
    return result_text if result_text else "Nenhuma resposta gerada."

def update_policies():
    cached_policies = None

    # Atualiza as políticas
    getPolicies()

# Rota da API para receber o CNPJ e gerar a análise
@app.post("/analyze/{cnpj}")
def analyze_cnpj(cnpj: str):
    try:
        result = generate_analysis(cnpj)
        return {"analysis": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Para rodar a API:
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

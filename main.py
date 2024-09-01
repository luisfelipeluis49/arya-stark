# main.py - Arquivo para a API FastAPI
from fastapi import FastAPI, HTTPException
from numpy import empty
from pydantic import BaseModel
from vertexai.generative_models import GenerativeModel, SafetySetting
import uvicorn
import vertexai
from bqget import bqget_instance  # Importando a instância da classe BQGet
from client_data_generator import generate_client_data  # Importando a função de geração de dados

app = FastAPI()

# Configuração do projeto Vertex AI
PROJECT_ID = "arya-hackathon"
LOCATION = "us-central1"
MODEL_NAME = "gemini-1.5-flash-001"

# Configuração do modelo e safety settings
generation_config = {
    "max_output_tokens": 1000,
    "temperature": 0.5,
    "top_p": 0.95,
}

cached_analysis = {}

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

# Modelo de entrada para o CNPJ
class CNPJInput(BaseModel):
    cnpj: str

# Função para gerar a análise com base no CNPJ e nas políticas
def generate_analysis(cnpj_input: str):
    client_data = generate_client_data(cnpj_input)  # Gera os dados fictícios do cliente com base no CNPJ
    last_policy = bqget_instance.get_policies()[-1] if bqget_instance.get_policies() else "Nenhuma política encontrada"
    
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = GenerativeModel(MODEL_NAME, system_instruction=(
        f"""Você é um auxiliar de onboarding de clientes do StarkBank e atende como copilot ao head de vendas;onboarding do banco. Com base no JSON de análise do cliente: {client_data} e a política de Critério Mínimo de Aceitação (CMA): {last_policy}, faça a análise de maneira objetiva e concisa. Caso alguma informação não seja encontrada, somente a ignore. O objetivo é avaliar o risco financeiro e operacional do cliente para o banco StarkBank.
        O resultado final deve ser em JSON com as chaves 'classificacao_risco' e 'pontos_atencao'.
        NÃO QUERO UMA SUGESTÃO DE ATUAÇÃO, APENAS A ANÁLISE DE RISCO COM A RESPOSTA DE SIM OU NÃO E UM SCORE."""
    ))

    text1 = f"""
    O cliente que estamos avaliando possui o CNPJ: {cnpj_input}.

    Com base nos dados coletados, faça uma análise completa sobre o risco trazer essa empresa para o banco, um risco financeiro deste cliente para o Stark Bank, considerando o contexto atual:

    - Informações Cadastrais: Razão social, situação cadastral, composição societária, e tempo de mercado.
    - Saúde Financeira: Balanço patrimonial, demonstração de resultados, fluxo de caixa, endividamento, score de crédito e histórico de pagamentos.
    - Compliance: Presença em listas de sanções ou registros de atividades irregulares.
    - Comportamento de Transações: Padrões de movimentação financeira, frequência e valores transacionados.

    Com base nesses dados, de breves insights sobre a empresa, responda às seguintes perguntas:
    1. Qual é a classificação de risco deste cliente?
    2. Quais são os principais pontos de atenção em relação ao risco financeiro e operacional?

    Considere todos os dados fornecidos e seja específico em sua análise, identificando se compensa ou não trazer essa empresa para o banco. Seja conciso e objetivo em suas respostas e gere uma nota final de 1 a 5, sendo 5 o maior risco que pode ser classificado.
    """

    response = model.generate_content(
        [text1],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=False,
    )

    cached_analysis[cnpj_input] = response

    result_text = response.text
    return result_text if result_text else "Nenhuma resposta gerada."

# Rota da API para receber o CNPJ e gerar a análise
@app.post("/analyze")
def analyze_cnpj(input_data: CNPJInput):
    try:
        result = generate_analysis(input_data.cnpj)
        return {"analysis": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Rota da API para receber o CNPJ e gerar a análise
@app.get("/analyze/{cnpj}")
def get_analysis(cnpj: str):
    try:
        result = generate_analysis(cnpj)
        return {"analysis": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Rota para atualizar as políticas no BigQuery e no cache
@app.post("/policies")
def update_policy(new_policy):
    try:
        update_response = bqget_instance.update_policies(new_policy)
        return update_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Rota para pegar as políticas no BigQuery e no cache
@app.get("/policies")
def get_policy(new_policy):
    try:
        get_response = bqget_instance.get_policies()
        return get_response;
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Para rodar a API
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

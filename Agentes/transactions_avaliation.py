'''
Recebe o id ou nome de um cliente presente em sua base de compras registradas.
Realiza 3 buscas no banco, utilizando 3 critérios avaliativos para atribuir a cada um uma nota de avaliação para os seguintes quesitos padrões:
    (1) A flutuação sobre a quantidade de transações de uma empresa ao longo dos dias
    (2) A flutuação positiva sobre o montante adquirido oa longo do tempo
    (3) Quantidade de compras com sucesso ao longo do tempo
'''

import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting
from google.cloud import bigquery
import warnings
warnings.filterwarnings("ignore")

example_client_name = "AWS"
PROJECT_ID = "arya-hackathon"
default_parameter_1 = "The fluctuation in the number of transactions of a company over the days must be overall increasing overall to be positive."
default_parameter_2 = "Number of successful purchases over time."
AVALIATION_PARAMETERS = [default_parameter_1, default_parameter_2]
RATING_WEIGHT = 5

generation_config = {
    "max_output_tokens": 3,
    "temperature": 0.6,
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


def initialize_vertex_ai(project: str, location: str):
    vertexai.init(project=project, location=location)


def create_generative_model(model_name: str, system_instruction: str = None) -> GenerativeModel:
    instruction = system_instruction if system_instruction else ""
    return GenerativeModel(model_name, system_instruction=[instruction])


def generate_content(model: GenerativeModel, question: str, generation_config, safety_settings) -> list:
    responses = model.generate_content(
        [question],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )
    return [response.text for response in responses]


def get_gemini_answer(question_string: str, system_instruction: str = None) -> list:
    model = create_generative_model("gemini-1.5-flash-001", system_instruction)
    try:
        responses = generate_content(model, question_string, generation_config, safety_settings)
        return responses
    except Exception as e:
        print(f"Error generating content: {e}")
        return []


def get_bigquery_purchase_data(seller_name:str=None, seller_id:str=None):
    assert seller_name is not None or seller_id is not None, "You must inform either a name or id for the seller to be searched for"
    query = f"""
        SELECT 
          FORMAT_DATE('%Y-%m', CAST(purchase_created AS DATE)) AS created, 
          purchase_status,
          COUNT(id) AS transactions_count 
        FROM `arya-hackathon.stark_mock.corporate_purchase`
        WHERE TRUE
            AND (--seller_name --seller_id)
        GROUP BY 1,2
        ORDER BY 1;
    """

    if seller_name and seller_id:
        query = query.replace("--seller_id", f"CAST(purchase_workspaceId AS STRING) = '{seller_id}'")
        query = query.replace("--seller_name", f" OR purchase_merchantName = '{seller_name}'")
    else:
        if seller_name:
            query = query.replace("--seller_name", f"purchase_merchantName = '{seller_name}'")
            query = query.replace("--seller_id", "")
        else:
            query = query.replace("--seller_id", f"CAST(purchase_workspaceId AS STRING) = '{seller_id}'")
            query = query.replace("--seller_name","")
    client = bigquery.Client(PROJECT_ID)
    query_job = client.query(query)
    results = query_job.result()
    df = results.to_dataframe()
    data = df.to_dict(orient='list')
    return data


def generate_potential_risk_grade(avaliation_parameter:str, database_data:str):
    prompt = database_data
    system_instruction = "Analyze whether the fluctuation in the purchase data of a company meets the following evaluation criteria and respond exactly with a score between 1 to 10 only: " \
                         + avaliation_parameter
    avaliation_grade = get_gemini_answer(question_string=prompt, system_instruction=system_instruction)[0]
    try:
        return (10 - float(avaliation_grade)) * RATING_WEIGHT
    except Exception:
        return -1


def get_transactions_all_avaliations():
    initialize_vertex_ai(project=PROJECT_ID, location="us-central1")

    purchase_data = get_bigquery_purchase_data(seller_name=example_client_name)
    risk_grades = []
    for parameter in AVALIATION_PARAMETERS:
        risk_grade = generate_potential_risk_grade(parameter, str(purchase_data))
        if risk_grade == -1:
            print("Skipping grade for parameter: " + parameter)
            continue
        risk_grades.append(risk_grade)
    return risk_grades


if __name__ == "__main__":
    print(get_transactions_all_avaliations())

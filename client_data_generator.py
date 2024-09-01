# client_data_generator.py
from faker import Faker
import random

# Inicializando o Faker com a localidade do Brasil para gerar dados mais realistas
faker = Faker('pt_BR')

def generate_client_data(cnpj):
    """
    Gera dados fictícios de cliente com base em um CNPJ utilizando o Faker.
    """
    client_data = {
        "CNPJ": cnpj,
        "Razao_Social": faker.company(),
        "Nome_Fantasia": faker.company_suffix(),
        "Endereco": {
            "Rua": faker.street_name(),
            "Numero": faker.building_number(),
            "Bairro": faker.neighborhood(),
            "Cidade": faker.city(),
            "Estado": faker.estado_sigla(),
            "CEP": faker.postcode(),
        },
        "Contato": {
            "Telefone": faker.phone_number(),
            "Email": faker.company_email(),
        },
        
        "Ramo de Atividade": faker.bs(),
        "Data de Fundacao": faker.date_this_century(),
        "Capital Social": f"R$ {faker.random_int(10000, 1000000)}",
        "Faturamento Anual": f"R$ {faker.random_int(10000, 1000000)}",
        "Funcionarios": faker.random_int(1, 100),
        "Site": faker.url(),
        "Socios": [
            {
                "Nome": faker.name(),
                "CPF": faker.cpf(),
                "Email": faker.email(),
                "Telefone": faker.phone_number(),
            },
            {
                "Nome": faker.name(),
                "CPF": faker.cpf(),
                "Email": faker.email(),
                "Telefone": faker.phone_number(),
            },
        ],

        "Risco de Crédito": {
            "Score de Crédito": random.randint(300, 850),
            "Endividamento": random.choice(['Alto', 'Moderado', 'Baixo']),
        },
        "Fluxo de Caixa": {
            "Fluxo de Caixa": random.choice(['positivo', 'negativo']),
            "Liquidez Imediata": random.choice(['alta', 'baixa']),
        },

        "Risco Financeiro": {
            "Saude Financeira": f"Score de crédito: {random.randint(300, 850)}, Endividamento: {random.choice(['Alto', 'Moderado', 'Baixo'])}",
            "Fluxo de Caixa": f"Fluxo de caixa {random.choice(['positivo', 'negativo'])}, liquidez imediata {random.choice(['alta', 'baixa'])}.",
        },
        "Risco Operacional": {
            "Falhas Operacionais": f"Ocorrência de falhas operacionais: {random.randint(0, 5)} incidentes nos últimos 12 meses.",
            "Dependencia de Fornecedores": f"Dependência de fornecedores críticos: {random.choice(['Alta', 'Moderada', 'Baixa'])}.",
        },
        "Risco Legal e Regulatório": {
            "Multas Recentes": f"Multas recentes: {random.randint(0, 3)}.",
            "Processos Judiciais": f"Envolvimento em processos legais: {random.choice(['Sim', 'Não'])}.",
        },
        "Risco de Reputação": {
            "Imagem Publica": f"Sentimento público: {random.choice(['Positivo', 'Negativo', 'Neutro'])} baseado em redes sociais.",
            "Mídia": f"Exposição na mídia: {random.choice(['Alta', 'Moderada', 'Baixa'])}.",
        },
        "Risco de Mercado": {
            "Exposicao a Concorrencia": f"Exposição à concorrência: {random.choice(['Alta', 'Moderada', 'Baixa'])}.",
            "Sensibilidade a Precos": f"Sensibilidade a preços de mercado: {random.choice(['Alta', 'Moderada', 'Baixa'])}.",
        },
        "Risco Tecnológico": {
            "Ciberseguranca": f"Vulnerabilidades em cibersegurança: {random.choice(['Sim', 'Não'])}.",
            "Infraestrutura TI": f"Infraestrutura de TI {random.choice(['atualizada', 'desatualizada'])}.",
        },
        "Risco Ambiental e Social": {
            "Impacto Ambiental": f"Impacto ambiental {random.choice(['positivo', 'negativo'])}.",
            "Iniciativas Sociais": f"Iniciativas sociais {random.choice(['presentes', 'ausentes'])}.",
        },
        "Ultimas Noticias": [
            {
                "Titulo": faker.sentence(),
                "Resumo": faker.text(),
                "Link": faker.url(),
            },
            {
                "Titulo": faker.sentence(),
                "Resumo": faker.text(),
                "Link": faker.url(),
            },
        ],
    }
    
    return client_data

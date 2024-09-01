import pandas as pd
import random
import numpy as np

# Definindo categorias e setores
categories = ['Grande Porte', 'Médio Porte', 'Pequeno Porte']
sectors = ['Varejo', 'Tecnologia', 'Serviços Financeiros', 'Transporte', 'Manufatura', 'Consultoria', 'Saúde']

# Função ajustada para gerar dados de clientes com base na categoria, setor, e valor médio das transações ajustados para tamanhos menores
def generate_clients_data_refined_with_smaller_transaction_value(num_clients):
    data = []
    for _ in range(num_clients):
        client_id = f"CLI{random.randint(1000, 9999)}"
        category = random.choice(categories)
        sector = random.choice(sectors)
        
        # Ajustes baseados na categoria e setor para Revenue e NumTransactions com valores menores
        if category == 'Grande Porte':
            base_revenue = random.uniform(20, 50) * 10**6  # Receita em milhões de 20 a 50
            base_transactions = random.randint(2000, 5000)  # Transações de 2000 a 5000
        elif category == 'Médio Porte':
            base_revenue = random.uniform(5, 20) * 10**6  # Receita em milhões de 5 a 20
            base_transactions = random.randint(500, 2000)  # Transações de 500 a 2000
        else:  # Pequeno Porte
            base_revenue = random.uniform(0.5, 5) * 10**6  # Receita em milhões de 0.5 a 5
            base_transactions = random.randint(50, 500)  # Transações de 50 a 500
        
        # Ajustando receita e transações com base no setor
        if sector == 'Tecnologia':
            revenue = base_revenue * random.uniform(1.1, 1.4)
            num_transactions = int(base_transactions * random.uniform(0.7, 1.1))
        elif sector == 'Serviços Financeiros':
            revenue = base_revenue * random.uniform(1.2, 1.5)
            num_transactions = int(base_transactions * random.uniform(0.8, 1.2))
        elif sector == 'Varejo':
            revenue = base_revenue * random.uniform(0.8, 1.1)
            num_transactions = int(base_transactions * random.uniform(1.0, 1.5))
        elif sector == 'Saúde':
            revenue = base_revenue * random.uniform(0.9, 1.2)
            num_transactions = int(base_transactions * random.uniform(0.9, 1.3))
        elif sector == 'Transporte':
            revenue = base_revenue * random.uniform(0.7, 1.0)
            num_transactions = int(base_transactions * random.uniform(1.0, 1.3))
        elif sector == 'Consultoria':
            revenue = base_revenue * random.uniform(0.9, 1.1)
            num_transactions = int(base_transactions * random.uniform(0.5, 0.9))
        else:  # Manufatura
            revenue = base_revenue * random.uniform(0.8, 1.2)
            num_transactions = int(base_transactions * random.uniform(0.9, 1.3))
        
        # Definindo o valor médio das transações (evitando divisão por zero)
        avg_transaction_value = revenue / max(num_transactions, 1)
        
        risk_score = round(random.uniform(0, 1), 2)  # Score de risco entre 0 (baixo) e 1 (alto)
        
        data.append([client_id, category, sector, revenue, num_transactions, avg_transaction_value, risk_score])
        
    return pd.DataFrame(data, columns=['ClientID', 'Category', 'Sector', 'Revenue', 'NumTransactions', 
                                       'AvgTransactionValue', 'RiskScore'])

# Gerando uma base de dados refinada com 10.000 clientes ajustados para tamanhos menores
clients_data_10000_refined = generate_clients_data_refined_with_smaller_transaction_value(10000)

# Função para calcular riscos com base nos parâmetros da empresa e adicionar erros aleatórios
def simulate_risks(row):
    # Definindo parâmetros básicos com base na categoria, receita e número de transações
    if row['Category'] == 'Grande Porte':
        financial_risk = 2
        operational_risk = 3
        tech_risk = 3
    elif row['Category'] == 'Médio Porte':
        financial_risk = 3
        operational_risk = 2
        tech_risk = 2
    else:  # Pequeno Porte
        financial_risk = 4
        operational_risk = 1
        tech_risk = 1
    
    # Ajustando riscos com base na receita da empresa
    if row['Revenue'] > 50 * 10**6:
        financial_risk -= 1  # Receita maior reduz o risco financeiro
        reputation_risk = 3
    else:
        reputation_risk = 2
    
    # Ajustando riscos com base no número de transações
    if row['NumTransactions'] > 5000:
        operational_risk += 1  # Mais transações aumentam o risco operacional
        legal_risk = 3
    else:
        legal_risk = 2
    
    # Ajustando o risco ESG
    esg_risk = random.choice([1, 2, 3, 4, 5])  # Valores variáveis para simular a diversidade dos riscos ESG
    
    # Adicionando erros aleatórios para simular variações reais
    random_error = np.random.normal(0, 0.5)  # Erro com média 0 e desvio padrão de 0.5
    
    # Aplicando erros aleatórios e garantindo que os valores fiquem entre 1 e 5
    financial_risk = max(1, min(5, financial_risk + random_error))
    operational_risk = max(1, min(5, operational_risk + random_error))
    legal_risk = max(1, min(5, legal_risk + random_error))
    reputation_risk = max(1, min(5, reputation_risk + random_error))
    tech_risk = max(1, min(5, tech_risk + random_error))
    esg_risk = max(1, min(5, esg_risk + random_error))
    
    return financial_risk, operational_risk, legal_risk, reputation_risk, tech_risk, esg_risk

# Aplicando a função de simulação de riscos para todos os clientes
clients_data_10000_refined[['RiskValue_Financial', 'RiskValue_Operational', 'RiskValue_Legal', 
                            'RiskValue_Reputation', 'RiskValue_Tech', 'RiskValue_ESG']] = clients_data_10000_refined.apply(simulate_risks, axis=1, result_type='expand')

# Criando probabilidades aleatórias para cada risco
clients_data_10000_refined['Probability_Financial'] = np.random.randint(1, 6, len(clients_data_10000_refined))
clients_data_10000_refined['Probability_Operational'] = np.random.randint(1, 6, len(clients_data_10000_refined))
clients_data_10000_refined['Probability_Legal'] = np.random.randint(1, 6, len(clients_data_10000_refined))
clients_data_10000_refined['Probability_Reputation'] = np.random.randint(1, 6, len(clients_data_10000_refined))
clients_data_10000_refined['Probability_Tech'] = np.random.randint(1, 6, len(clients_data_10000_refined))
clients_data_10000_refined['Probability_ESG'] = np.random.randint(1, 6, len(clients_data_10000_refined))

# Pesos constantes para cada risco, aplicáveis a todos os clientes
weight_financial = 5
weight_operational = 4
weight_legal = 3
weight_reputation = 5
weight_tech = 4
weight_esg = 3

# Função para calcular o risco total
def calculate_total_risk(row):
    total_risk = (
        (row['RiskValue_Financial'] * row['Probability_Financial'] * weight_financial) +
        (row['RiskValue_Operational'] * row['Probability_Operational'] * weight_operational) +
        (row['RiskValue_Legal'] * row['Probability_Legal'] * weight_legal) +
        (row['RiskValue_Reputation'] * row['Probability_Reputation'] * weight_reputation) +
        (row['RiskValue_Tech'] * row['Probability_Tech'] * weight_tech) +
        (row['RiskValue_ESG'] * row['Probability_ESG'] * weight_esg)
    )
    return total_risk

# Aplicando o cálculo do risco total
clients_data_10000_refined['TotalRisk'] = clients_data_10000_refined.apply(calculate_total_risk, axis=1)

# Definindo um limite de risco para aceitação
risk_threshold = 75  # Exemplo de limite arbitrário

# Avaliação final com base no risco total
clients_data_10000_refined['Status'] = clients_data_10000_refined['TotalRisk'].apply(
    lambda x: 'Aprovada' if x <= risk_threshold else 'Rejeitada - Risco Elevado'
)

# Função para calcular o lucro estimado com base no valor médio das transações
def calculate_profit_with_value(row):
    total_transactions = row['NumTransactions']
    avg_value = row['AvgTransactionValue']
    
    # Definindo proporções para cada tipo de transação
    proportion_boleto = 0.10
    proportion_qr_code = 0.30
    proportion_pix = 0.30
    proportion_ted = 0.20
    proportion_pix_key = 0.10
    
    # Calculando o número estimado de cada tipo de transação
    transactions_boleto = total_transactions * proportion_boleto
    transactions_qr_code = total_transactions * proportion_qr_code
    transactions_pix = total_transactions * proportion_pix
    transactions_ted = total_transactions * proportion_ted
    transactions_pix_key = total_transactions * proportion_pix_key
    
    # Calculando o lucro para cada tipo de transação considerando o valor médio
    profit_boleto = transactions_boleto * 0.00 * avg_value
    profit_qr_code = transactions_qr_code * 0.50 * avg_value
    profit_pix = transactions_pix * 0.50 * avg_value
    profit_ted = transactions_ted * 2.00 * avg_value
    profit_pix_key = transactions_pix_key * 0.15 * avg_value
    
    # Somando o lucro total e subtraindo um custo fixo de R$ 1000
    total_profit = random.uniform(0.9, 1.1) * (profit_qr_code + profit_pix + profit_ted + profit_pix_key - 1000)
    
    return total_profit

# Aplicando o cálculo do lucro estimado com valor das transações
clients_data_10000_refined['EstimatedProfit'] = clients_data_10000_refined.apply(calculate_profit_with_value, axis=1)

# Salvando os dados atualizados em um arquivo CSV
clients_data_10000_refined.to_csv('clientes_risco_simulado_refinado_com_valor_transacao.csv', index=False)

print("Arquivo 'clientes_risco_simulado_refinado_com_valor_transacao_ajustado.csv' salvo com sucesso.")


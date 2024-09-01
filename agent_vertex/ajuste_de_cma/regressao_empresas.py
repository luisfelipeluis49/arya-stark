from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pandas as pd

# Carregar os dados do CSV gerado
data = pd.read_csv('clientes_risco_simulado_refinado_com_valor_transacao.csv')

# Seleção das features (variáveis independentes) e do target (variável dependente)
features = data[['Category', 'Sector', 'Revenue', 'NumTransactions', 'AvgTransactionValue', 'TotalRisk']]
target = data['EstimatedProfit']

# Divisão dos dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Definição das colunas categóricas e numéricas para o pré-processamento
categorical_features = ['Category', 'Sector']
numeric_features = ['Revenue', 'NumTransactions', 'AvgTransactionValue', 'TotalRisk']

# Pré-processamento: One-Hot Encoding para categóricas
preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', numeric_features),
        ('cat', OneHotEncoder(), categorical_features)
    ])

# Definindo o modelo de Ridge Regression com regularização
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', Ridge(alpha=1.0))  # alpha controla o grau de regularização; ajustável conforme necessário
])

# Treinamento do modelo
model.fit(X_train, y_train)

# Avaliação do modelo usando validação cruzada para evitar overfitting
cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
print(f'Score médio na validação cruzada: {cv_scores.mean() * 100:.2f}%')

# Avaliando o modelo no conjunto de teste
y_pred = model.predict(X_test)
accuracy = r2_score(y_test, y_pred) * 100
print(f'Precisão do Modelo no Conjunto de Teste: {accuracy:.2f}%')

# Exemplo de previsão para um novo cliente
new_client = pd.DataFrame([['Médio Porte', 'Tecnologia', 50000000, 1500, 33000, 180]],
                          columns=['Category', 'Sector', 'Revenue', 'NumTransactions', 'AvgTransactionValue', 'TotalRisk'])
predicted_profit = model.predict(new_client)

print(f'Lucro Estimado para o Novo Cliente: R$ {predicted_profit[0]:.2f}')

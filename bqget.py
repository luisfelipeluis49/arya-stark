# bqget.py - Classe para gerenciar o cache e as interações com BigQuery
from pickle import GET
from google.cloud import bigquery

class BQGet:
    def __init__(self):
        self.cached_policies = None

    def get_policies(self):
        """
        Busca as políticas do BigQuery se o cache estiver vazio.
        """
        if self.cached_policies is None:
            # Exemplo de como você buscaria as políticas do BigQuery
            # Ajuste a consulta conforme o schema e tabela real
            client = bigquery.Client()
            query = "SELECT POLITICA FROM `arya-hackathon.stark_mock.cma_policy` ORDER BY INSERT_DATE DESC LIMIT 1"  # Ajuste conforme a tabela
            query_job = client.query(query)
            result = query_job.result()
            self.cached_policies = [row for row in result]  # Exemplo de conversão dos resultados para lista
        
        return self.cached_policies
    
    def get_next_id(self, client, table_id):
        """
        Obtém o próximo ID para inserção baseado no maior ID existente.
        """
        query = f"SELECT MAX(ID) as max_id FROM {table_id}"
        query_job = client.query(query)
        result = query_job.result()
        max_id = 0
        for row in result:
            if row.max_id is not None:
                max_id = row.max_id
        return max_id + 1

    def update_policies(self, new_policy: str):
        """
        Atualiza o cache das políticas e persiste no BigQuery com um ID incremental.
        """
        client = bigquery.Client()
        table_id = "arya-hackathon.stark_mock.cma_policy"
        
        # Obtém o próximo ID para inserção
        next_id = self.get_next_id(client, table_id)

        # Prepara os dados para inserção (sem a necessidade de passar a data)
        rows_to_insert = [
            {"ID": next_id, "POLITICA": new_policy}
        ]
        
        # Inserir nova política no BigQuery
        errors = client.insert_rows_json(table_id, rows_to_insert)
        if errors:
            print(f"Erro ao inserir novas políticas no BigQuery: {errors}")
            return {"status": "error", "message": errors}
        
        # Atualize o cache após inserir no BigQuery
        self.cached_policies = self.get_policies()
        return {"status": "success", "message": "Política atualizada com sucesso!"}
    
bqget_instance = BQGet()
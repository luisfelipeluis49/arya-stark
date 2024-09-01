# Agentes

O conceito de agentes é amplamente utilizado em inteligência artificial, onde um agente é um sistema que percebe o ambiente e age sobre ele. A ideia é que o agente possa receber uma tarefa específica e, a partir disso, tomar decisões para alcançar o objetivo. Para o desenvolvimento dos agentes, criamos dois tipos: o agente qualitativo e o agente quantitativo.

## Agente de Risco Reputacional

Este agente é responsável por avaliar dados qualitativos provenientes de diversas fontes. Para o teste de conceito, desenvolvemos um crawler que coleta informações a partir de pesquisas no Google, acessa os sites e extrai os dados relevantes. Realizamos esse processo para os primeiros 50 resultados da pesquisa, e, a partir daí, o agente envia as informações para o modelo de LLM, que gera uma análise coerente e consistente sobre a reputação do cliente, com base nos atributos da empresa.

## Agente de Risco Financeiro

Este agente é responsável por avaliar dados quantitativos provenientes de diversas fontes, como BACEN, SERASA, SPC, entre outras. Para o teste de conceito, utilizamos dados fictícios gerados por meio da biblioteca Faker. A partir desses dados, o agente envia as informações para o modelo de LLM, que gera uma análise coerente e consistente sobre o risco financeiro do cliente, com base nos atributos da empresa.

Ambos os agentes são responsáveis por gerar uma pontuação baseada no due diligence, e ambos apresentaram excelentes resultados, mesmo com alterações nos atributos da empresa, mantendo a consistência nos resultados respeitando as alterações nos atributos e gerando novas análises coerentes.

Caso queria testar os agentes, o arquivo `agentes.py` contém o código para a execução dos agentes.

## Implementação

A proposta de uma implementação eficiente dos agentes é sua execução em lambda functions na AWS ou seu equivalente na Google Cloud. A proposta é que os agentes sejam executados em um ambiente serverless, onde a execução é feita sob demanda, sem a necessidade de manter um servidor ativo. Isso permite que os agentes sejam executados de forma rápida e eficiente, sem a necessidade de manter um servidor ativo, reduzindo custos e aumentando a eficiência da execução.
O orquestrador dos agentes tambem pode ser implementado em uma lambda function, onde ele é responsável por orquestrar a execução dos agentes, garantindo que os agentes sejam executados de forma eficiente retorne os resultados esperados para que o modelo de LLM possa gerar as análises coerentes e consistentes de todos os dados coletados.

![Agentes](imagem/FluxoDeD.jpg)

Mesmo os exemplos dos agentes sendo realizados com LLM's a proposta é que os agentes possam ser utilizados com qualquer modelo, inclusive utilizando uma programação seguencial, onde o agente qualitativo e quantitativo podem ser executados de forma sequencial, garantindo que os dados sejam coletados e enviados para o modelo de LLM de forma eficiente e rápida.




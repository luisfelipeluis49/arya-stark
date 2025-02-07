# Arya

Based on the client's transactional data, interactions with the institution, and due diligence criteria, we propose new evaluation policies for the institution. The goal is to facilitate the maintenance of analysis for existing client profiles and the onboarding of new clients by integrating relevant information through third-party APIs or the institution itself.

## The Agents

Currently, most companies use qualitative policies to evaluate quantitative data from various internal or external sources. To support this process, we have developed two agents: one to process and evaluate qualitative data and another for quantitative data. The creation of these agents demonstrates the effectiveness of LLMs (Large Language Models), generating coherent and consistent analyses based on the company’s policies while also providing a due diligence-based scoring system. For more details about the agents, refer to the respective folder where a detailed explanation is provided.

![Agentes](imagem/FluxoDeD.jpg)

# Copilot

The primary AI used in the project is the `Policy Validator`, responsible for receiving data analyzed by the due diligence module and, in conjunction with client performance evaluations, applying an architecture similar to that used in due diligence. However, in this case, the institution’s own information is used to assess relevant transactions, such as money laundering, fraud, and other risks. 

![Copilot](imagem/FluxoCopilot.jpg)

We understand that this agent may require fine-tuning since the data we aim to evaluate is highly specific. However, even without this procedure, we simulated its application and achieved promising results with an LLM that was fed client information, previous policies, and behavioral analyses. This allowed the LLM to generate plausible policies. With a larger volume of data and proper fine-tuning, the results are even more promising.

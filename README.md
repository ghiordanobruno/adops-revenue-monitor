# adops-revenue-monitor

Pipeline em Python para simular o monitoramento diário de receita publicitária digital. O projeto gera dados sintéticos de AdOps, aplica validações de qualidade, calcula métricas de monetização, identifica anomalias operacionais e exporta um dashboard em Excel para análise.

A proposta é reproduzir uma rotina de apoio a AdOps: acompanhar indicadores, encontrar inconsistências, investigar variações fora do esperado e organizar uma visão clara de performance para tomada de decisão.

## Problema simulado

Times de AdOps e monetização precisam acompanhar diariamente se a entrega de anúncios está saudável. Quedas de preenchimento, receita zerada, CTR fora do padrão ou inconsistências entre requisições, impressões e cliques podem indicar falhas de tagueamento, problemas de demanda, bugs de mensuração ou mudanças bruscas de performance.

Este projeto simula esse cenário com dados fictícios e separa o processo em etapas independentes para facilitar leitura, manutenção e validação.

## Objetivos do projeto

- Criar uma base de dados sintética com performance diária de anúncios.
- Organizar um pipeline simples e reproduzível em Python.
- Tratar duplicidades, valores ausentes e tipos incorretos.
- Calcular indicadores de entrega, engajamento e receita.
- Detectar anomalias comuns em dados de AdOps.
- Exportar um arquivo Excel final para análise e apresentação.

## Pipeline

O fluxo principal está em [run_pipeline.py](run_pipeline.py):

1. Geração dos dados brutos com [generate_sample_data.py](generate_sample_data.py).
2. Limpeza e padronização da base com [clean_data.py](clean_data.py).
3. Cálculo das métricas com [calculate_metrics.py](calculate_metrics.py).
4. Detecção de anomalias com [detect_anomalies.py](detect_anomalies.py).
5. Exportação do dashboard em Excel com [export_dashboard.py](export_dashboard.py).

Cada etapa também pode ser executada de forma independente, o que facilita depuração, manutenção e leitura do código.

## Documentação dos scripts

- `generate_sample_data.py`: [docs/generate_sample_data.md](docs/generate_sample_data.md)
- `clean_data.py`: [docs/clean_data.md](docs/clean_data.md)
- `calculate_metrics.py`: [docs/calculate_metrics.md](docs/calculate_metrics.md)
- `detect_anomalies.py`: [docs/detect_anomalies.md](docs/detect_anomalies.md)
- `export_dashboard.py`: [docs/export_dashboard.md](docs/export_dashboard.md)

## Estrutura do projeto

```text
adops-revenue-monitor/
├── data/
│  ├── raw/
│  └── processed/
├── docs/
├── reports/
├── generate_sample_data.py
├── clean_data.py
├── calculate_metrics.py
├── detect_anomalies.py
├── export_dashboard.py
├── run_pipeline.py
├── requirements.txt
└── README.md
```

## Base de dados

A base gerada contém pelo menos 90 dias de dados fictícios com as colunas:

- `date`
- `site_section`
- `device`
- `country`
- `ad_unit`
- `ad_requests`
- `matched_requests`
- `impressions`
- `clicks`
- `estimated_revenue`

O gerador também inclui alguns problemas controlados, como duplicidades, valores ausentes e inconsistências lógicas. Isso permite demonstrar limpeza de dados e validações.

## Métricas calculadas

- `match_rate`: `matched_requests / ad_requests`
- `fill_rate`: `impressions / matched_requests`
- `ctr`: `clicks / impressions`
- `rpm`: `(estimated_revenue / ad_requests) * 1000`
- `ecpm`: `(estimated_revenue / impressions) * 1000`

Neste projeto, `rpm` foi definido como receita estimada por mil ad requests, para acompanhar eficiência de monetização sobre a demanda recebida. Já `ecpm` foi definido como receita estimada por mil impressões, aproximando a métrica do rendimento sobre anúncios efetivamente exibidos.

As taxas são gravadas como valores decimais. Por exemplo, `0.70` representa 70%.

## Regras de anomalia

O script [detect_anomalies.py](detect_anomalies.py) identifica:

- `impressions_gt_matched_requests`: impressões maiores que requisições preenchidas.
- `clicks_gt_impressions`: cliques maiores que impressões.
- `zero_revenue_high_impressions`: receita igual a zero com pelo menos 1.000 impressões.
- `low_fill_rate`: `fill_rate` abaixo de 70%.
- `rpm_drop_gt_25pct_vs_7d_avg`: queda de `rpm` acima de 25% contra a média móvel anterior de 7 dias.
- `high_ctr`: `ctr` acima de 10%.

## Exemplos de anomalias detectadas

| Regra | Interpretação |
| --- | --- |
| `impressions_gt_matched_requests` | Possível inconsistência de mensuração ou erro na geração/coleta dos dados. |
| `clicks_gt_impressions` | Quantidade de cliques incompatível com o volume de impressões registrado. |
| `zero_revenue_high_impressions` | Inventário com entrega relevante, mas sem receita registrada. |
| `low_fill_rate` | Baixo aproveitamento das requisições preenchidas em impressões. |
| `rpm_drop_gt_25pct_vs_7d_avg` | Queda relevante de receita por mil requisições contra a média recente. |
| `high_ctr` | CTR fora do padrão esperado, possível sinal de erro de mensuração ou tráfego atípico. |

## Dashboard exportado

O arquivo final é salvo em:

```text
reports/adops_dashboard.xlsx
```

Ele contém as abas:

- `raw_data`: base bruta gerada.
- `clean_data`: base limpa e padronizada.
- `metrics`: base com métricas calculadas.
- `anomalies`: linhas marcadas por regras de anomalia.
- `summary`: agregações por data, seção do site, dispositivo e unidade de anúncio.

## Resultados gerados

Na execução padrão, o pipeline gera:

- Base bruta com registros diários por seção, dispositivo, país e unidade de anúncio.
- Base tratada com tipos padronizados, valores ausentes tratados e duplicidades removidas.
- Métricas de `match_rate`, `fill_rate`, `ctr`, `rpm` e `ecpm`.
- Lista de anomalias classificadas por regra de negócio.
- Arquivo Excel com abas de dados, métricas, anomalias e resumo agregado.

## Decisões técnicas

- Usei dados sintéticos para não depender de credenciais ou fontes proprietárias de plataformas de anúncios.
- Mantive o Excel como saída principal porque ele é comum em rotinas operacionais de análise, acompanhamento e apresentação de resultados.
- Usei regras explícitas de anomalia em vez de modelos estatísticos para facilitar auditoria e leitura por avaliadores técnicos e não técnicos.
- Separei o pipeline em etapas independentes para facilitar depuração, reuso e manutenção.
- Mantive os scripts pequenos e com funções específicas para deixar o fluxo mais claro.

## Como executar

Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
pip install -r requirements.txt
```

Execute o pipeline completo:

```powershell
python run_pipeline.py
```

Também é possível executar as etapas separadamente:

```powershell
python generate_sample_data.py
python clean_data.py
python calculate_metrics.py
python detect_anomalies.py
python export_dashboard.py
```

### Usando arquivos customizados

Os scripts aceitam parâmetros para informar caminhos de entrada e saída. Isso permite testar arquivos alternativos sem alterar o pipeline principal.

Gerar uma base bruta em outro caminho:

```powershell
python generate_sample_data.py --days 120 --seed 10 --output data/raw/adops_custom_raw.csv
```

Limpar um CSV específico usando `--input`:

```powershell
python clean_data.py --input data/raw/adops_custom_raw.csv --output data/processed/custom_clean_data.csv
```

Calcular métricas a partir de uma base limpa específica:

```powershell
python calculate_metrics.py --input data/processed/custom_clean_data.csv --output data/processed/custom_metrics.csv
```

Detectar anomalias a partir de um arquivo de métricas específico:

```powershell
python detect_anomalies.py --input data/processed/custom_metrics.csv --output data/processed/custom_anomalies.csv
```

Exportar o Excel usando arquivos específicos:

```powershell
python export_dashboard.py --raw data/raw/adops_custom_raw.csv --clean data/processed/custom_clean_data.csv --metrics data/processed/custom_metrics.csv --anomalies data/processed/custom_anomalies.csv --output reports/custom_adops_dashboard.xlsx
```

## Saídas geradas

- `data/raw/adops_performance_raw.csv`
- `data/processed/clean_data.csv`
- `data/processed/metrics.csv`
- `data/processed/anomalies.csv`
- `reports/adops_dashboard.xlsx`

## O que este projeto cobre

- Manipulação de dados com `pandas`.
- Exportação de relatórios em Excel com `openpyxl`.
- Criação de pipeline modular em Python.
- Validação e limpeza de dados.
- Cálculo de métricas de AdOps e monetização digital.
- Detecção de anomalias com regras de negócio.
- Organização de projeto para leitura.

## Limitações

- Os dados são sintéticos e não representam uma operação real.
- As regras de anomalia são heurísticas simples, não modelos estatísticos.
- O projeto não se conecta diretamente a plataformas como Google Ad Manager, AdSense ou SSPs.
- As métricas foram definidas para fins de simulação e podem variar conforme a plataforma usada.

## Possíveis evoluções

- Adicionar testes automatizados com `pytest`.
- Criar gráficos no Excel para RPM, receita e fill rate.
- Adicionar um preview visual do dashboard em `assets/dashboard_preview.png`.
- Adicionar alertas por e-mail ou Slack para anomalias críticas.
- Conectar o pipeline a uma fonte real, como Google Ad Manager, AdSense ou arquivos exportados de uma SSP.
- Criar uma versão em dashboard web com Streamlit ou Power BI.

# calculate_metrics.py

## Objetivo

Calcula métricas de AdOps e monetização digital a partir da base limpa.

## Entrada

Arquivo padrao:

```text
data/processed/clean_data.csv
```

Também aceita um caminho customizado com `--input`.

## Saída

Gera o arquivo:

```text
data/processed/metrics.csv
```

## Exemplo de uso

Execução padrão:

```powershell
python calculate_metrics.py
```

Usando uma base limpa customizada:

```powershell
python calculate_metrics.py --input data/processed/custom_clean_data.csv --output data/processed/custom_metrics.csv
```

## Métricas calculadas

- `match_rate`: `matched_requests / ad_requests`
- `fill_rate`: `impressions / matched_requests`
- `ctr`: `clicks / impressions`
- `rpm`: `(estimated_revenue * 1000) / ad_requests`
- `ecpm`: `(estimated_revenue * 1000) / impressions`

## Principais funções

- `parse_args()`: lê os caminhos de entrada e saida pelo terminal.
- `safe_divide(numerator, denominator)`: realiza divisões evitando erro quando o denominador é zero.
- `calculate_metrics(df)`: cria as colunas de metricas no DataFrame.
- `save_csv(df, output_path)`: salva o CSV com as metricas calculadas.
- `main()`: executa o calculo de métricas quando o arquivo é chamado diretamente.

## Observação

As taxas são salvas como decimais. Por exemplo, `0.70` representa 70%.

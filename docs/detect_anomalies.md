# detect_anomalies.py

## Objetivo

Identifica inconsistências e sinais de alerta na base com métricas calculadas.

## Entrada

Arquivo padrão:

```text
data/processed/metrics.csv
```

Também aceita um caminho customizado com `--input`.

## Saída

Gera o arquivo:

```text
data/processed/anomalies.csv
```

## Exemplo de uso

Execução padrão:

```powershell
python detect_anomalies.py
```

Usando um arquivo de métricas customizado:

```powershell
python detect_anomalies.py --input data/processed/custom_metrics.csv --output data/processed/custom_anomalies.csv
```

## Regras aplicadas

- Impressões maiores que `matched_requests`.
- Cliques maiores que impressões.
- Receita igual a zero com pelo menos 1.000 impressoes.
- `fill_rate` abaixo de 70%.
- Queda de `rpm` acima de 25% em relacao a media movel anterior de 7 dias.
- `ctr` acima de 10%.

## Principais funções

- `parse_args()`: lê os caminhos de entrada e saída pelo terminal.
- `add_rolling_rpm_average(df)`: calcula a média móvel anterior de 7 dias do `rpm`.
- `build_anomaly_rows(df, mask, anomaly_type, detail_builder)`: cria linhas de anomalia a partir de uma regra.
- `detect_anomalies(df)`: executa todas as regras e consolida as anomalias encontradas.
- `save_csv(df, output_path)`: salva o CSV de anomalias.
- `main()`: executa a detecção quando o arquivo é chamado diretamente.

## Observação

Uma mesma linha pode aparecer mais de uma vez no arquivo de anomalias se violar mais de uma regra.

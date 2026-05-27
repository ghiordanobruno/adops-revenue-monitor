# export_dashboard.py

## Objetivo

Exporta os dados do projeto para um arquivo Excel com abas separadas para análise.

## Entrada

Arquivos padrão:

```text
data/raw/adops_performance_raw.csv
data/processed/clean_data.csv
data/processed/metrics.csv
data/processed/anomalies.csv
```

Também aceita caminhos customizados com `--raw`, `--clean`, `--metrics` e `--anomalies`.

## Saída

Gera o arquivo:

```text
reports/adops_dashboard.xlsx
```

## Exemplo de uso

Execução padrão:

```powershell
python export_dashboard.py
```

Usando arquivos customizados:

```powershell
python export_dashboard.py --raw data/raw/adops_custom_raw.csv --clean data/processed/custom_clean_data.csv --metrics data/processed/custom_metrics.csv --anomalies data/processed/custom_anomalies.csv --output reports/custom_adops_dashboard.xlsx
```

## Abas do Excel

- `raw_data`: dados brutos gerados.
- `clean_data`: dados limpos.
- `metrics`: dados com métricas calculadas.
- `anomalies`: anomalias detectadas.
- `summary`: agregações por data, seção do site, device e ad unit.

## Principais funções

- `parse_args()`: lê os caminhos dos arquivos de entrada e saida.
- `aggregate_summary(metrics_df, group_columns)`: agrega os dados por uma dimensão e recalcula as métricas.
- `build_summary_tables(metrics_df)`: monta as tabelas usadas na aba `summary`.
- `write_summary_sheet(writer, summary_tables)`: escreve as tabelas de resumo no Excel.
- `autosize_columns(worksheet)`: ajusta a largura das colunas.
- `format_workbook(writer)`: aplica formatação básica nas abas.
- `export_dashboard(...)`: cria o arquivo Excel final.
- `main()`: executa a exportação quando o arquivo e chamado diretamente.

## Observação

Este arquivo usa `openpyxl` como engine de escrita e formatacao do Excel.

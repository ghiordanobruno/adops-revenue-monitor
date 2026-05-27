# clean_data.py

## Objetivo

Limpa e padroniza a base bruta gerada pelo projeto.

## Entrada

Arquivo padrão:

```text
data/raw/adops_performance_raw.csv
```

Tambem aceita um caminho customizado com `--input`.

## Saída

Gera o arquivo:

```text
data/processed/clean_data.csv
```

## Exemplo de uso

Execução padrão:

```powershell
python clean_data.py
```

Usando um arquivo de entrada customizado:

```powershell
python clean_data.py --input data/raw/adops_custom_raw.csv --output data/processed/custom_clean_data.csv
```

## Principais funcoes

- `parse_args()`: lê os caminhos de entrada e saída pelo terminal.
- `load_csv(input_path)`: carrega um CSV e valida se o arquivo existe.
- `validate_required_columns(df)`: confere se todas as colunas obrigaórias estão presentes.
- `normalize_categories(df)`: trata campos categoricos, remove espaços e preenche nulos com `unknown`.
- `normalize_dates(df)`: converte datas e remove registros com data inválida.
- `normalize_numeric_values(df)`: converte colunas numéricas, preenche nulos e remove valores negativos.
- `clean_data(df)`: aplica todo o processo de limpeza, remove duplicidades e ordena os dados.
- `save_csv(df, output_path)`: salva a base limpa em CSV.
- `main()`: executa a limpeza quando o arquivo é chamado diretamente.

## Observação

Este arquivo nao corrige inconsistências de negócio, como cliques maiores que impressões. Essas situacoes são mantidas para serem identificadas em `detect_anomalies.py`.

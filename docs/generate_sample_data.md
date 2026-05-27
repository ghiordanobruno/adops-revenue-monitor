# generate_sample_data.py

## Objetivo

Gera uma base fictícia de performance de anúncios digitais para simular uma rotina de AdOps.

## Entrada

O script não depende de arquivos de entrada. Ele recebe parâmetros opcionais pelo terminal:

- `--days`: quantidade de dias gerados. Padrao: `90`.
- `--seed`: seed aleatória para reproduzir os mesmos dados. Padrão: `42`.
- `--output`: caminho do CSV de saída.

## Saída

Gera o arquivo:

```text
data/raw/adops_performance_raw.csv
```

## Exemplo de uso

Execução padrão:

```powershell
python generate_sample_data.py
```

Gerando mais dias e salvando em outro caminho:

```powershell
python generate_sample_data.py --days 120 --seed 10 --output data/raw/adops_custom_raw.csv
```

## Principais funcoes

- `parse_args()`: lê os parametros informados no terminal.
- `build_date_range(days)`: cria a lista de datas usadas na base.
- `calculate_requests(...)`: calcula o volume ficticio de requisições de anúncio.
- `generate_rows(days, seed)`: monta as linhas da base com combinacoes de data, secao, device, pais e ad unit.
- `inject_sample_quality_issues(df, seed)`: adiciona duplicidades, valores ausentes e inconsistências controladas.
- `generate_sample_data(days, seed)`: gera o DataFrame bruto completo.
- `save_csv(df, output_path)`: salva o DataFrame em CSV.
- `main()`: executa o script quando chamado diretamente pelo terminal.

## Observação

As inconsistencias são intencionais. Elas existem para demonstrar as etapas posteriores de limpeza e detecção de anomalias.

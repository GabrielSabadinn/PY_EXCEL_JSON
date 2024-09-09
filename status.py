import pandas as pd
import json
import re
from datetime import datetime

# Caminho do arquivo de entrada
file_path = 'message.txt'

# Inicializar listas para armazenar os dados extraídos
data = {
    'datetime': [],
    'id': [],
    'totalValue': [],
    'dictCodeType': [],
    'dictCode': [],
    'Tags[0]': [],
    'status': [],  
    'transaction.endToEnd': [],
    'transaction.date': [],
}

# Função para extrair JSON de uma string
def extract_json_from_line(line):
    try:
        # Encontrar o JSON na linha
        json_str = re.search(r'\{.*\}', line)
        if json_str:
            return json.loads(json_str.group())
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return None

# Função para extrair data e hora
def extract_datetime_from_line(line):
    try:
        # Encontrar a data e hora no início da linha
        datetime_str = re.match(r'(\w{3} \d{2} \d{2}:\d{2}:\d{2})', line)
        if datetime_str:
            # Adicionar o ano (2024) à string da data e hora
            return datetime.strptime(f'2024 {datetime_str.group()}', '%Y %b %d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        print(f"Erro ao converter data e hora: {e}")
        return None

# Ler o arquivo
with open(file_path, 'r') as file:
    lines = file.readlines()

# Processar cada linha do arquivo
for line in lines:
    # Buscar JSON na linha
    data_dict = extract_json_from_line(line)
    
    # Extrair a data e hora
    datetime_str = extract_datetime_from_line(line)
    
    if data_dict:
        try:
            # Exibir dados JSON para depuração
            print(f"Dados JSON extraídos: {data_dict}")
            
            # Extrair as informações necessárias
            data['datetime'].append(datetime_str)  
            data['id'].append(data_dict.get('id', ''))
            data['totalValue'].append(data_dict.get('totalValue', ''))
            data['dictCodeType'].append(data_dict.get('dictCodeType', ''))
            data['dictCode'].append(data_dict.get('dictCode', ''))
            data['Tags[0]'].append(data_dict.get('tags', [])[0] if len(data_dict.get('tags', [])) > 0 else '')
          
            status = data_dict.get("                           status", '').strip()
            data['status'].append(status)
            data['transaction.endToEnd'].append(data_dict.get('transaction', {}).get('endToEnd', ''))
            data['transaction.date'].append(data_dict.get('transaction', {}).get('date', ''))
            
        except Exception as e:
            print(f"Erro ao processar JSON: {data_dict}")
            print(f"Erro: {e}")

# Verificar se todas as listas têm o mesmo comprimento
lengths = {len(lst) for lst in data.values()}
if len(lengths) > 1:
    print("Aviso: As listas em 'data' têm comprimentos diferentes:")
    for key, lst in data.items():
        print(f"{key}: {len(lst)}")
else:
    # Criar DataFrame
    df = pd.DataFrame(data)

    # Exibir DataFrame para depuração
    print("DataFrame resultante:")
    print(df)

    # Salvar em um arquivo Excel
    output_path = 'extracted_data.xlsx'
    try:
        df.to_excel(output_path, index=False)
        print(f"Dados extraídos e salvos em {output_path}")
    except PermissionError:
        print(f"Erro ao salvar o arquivo. Verifique se o arquivo está aberto ou se você tem permissões de gravação.")

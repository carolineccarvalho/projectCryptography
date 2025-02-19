import os
import pandas as pd
import csvs.anom.anonymization as anonymization

# Função para anonimizar o arquivo CSV
def anonymize_csv(input_file):
    print(input_file)
    df = pd.read_csv(input_file, on_bad_lines='skip', sep=";")

    # Verifique se as colunas _ws.col.SA e _ws.col.DA existem no dataframe
    if '_ws.col.SA' not in df.columns or '_ws.col.DA' not in df.columns:
        print(f"As colunas '_ws.col.SA' e '_ws.col.DA' não foram encontradas no arquivo {input_file}.")
        return

    # Anonimizar as colunas de IP
    df['_ws.col.SA_anonymized'] = df['_ws.col.SA'].apply(lambda ip: anonymization.encrypt(ip, 16))
    df['_ws.col.DA_anonymized'] = df['_ws.col.DA'].apply(lambda ip: anonymization.encrypt(ip, 16))

    # Salve o arquivo CSV com as colunas anonimizadas
    output_file = input_file.replace('.csv', '_anom.csv')
    df.to_csv(output_file, index=False)
    print(f"Arquivo com dados anonimizados salvo como: {output_file}")

# Função principal para anonimizar todos os arquivos CSV na pasta
def main():
    # Caminho da pasta onde os arquivos CSV estão
    folder_path = './csvs'  # ou coloque o caminho da pasta desejada, como './pasta_de_csv/'

    # Lista todos os arquivos na pasta
    for filename in os.listdir(folder_path):
        # Verifica se o arquivo tem extensão .csv
        if filename.endswith('.csv'):
            # Caminho completo do arquivo CSV
            input_file = os.path.join(folder_path, filename)
            anonymize_csv(input_file)

# Chamar a função principal
if __name__ == "__main__":
    main()

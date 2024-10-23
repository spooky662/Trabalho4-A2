import pandas as pd
import re
import matplotlib.pyplot as plt

# Função para ler o arquivo e criar o DataFrame
def ler_arquivo(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        linhas = file.readlines()

    dados = []
    pattern = r'(\d{2}/\d{2}/\d{4}) (\d{2}:\d{2}) - (.+)'

    for linha in linhas:
        match = re.match(pattern, linha)
        if match:
            data, hora, mensagem = match.groups()
            remetente_mensagem = mensagem.split(' ', 1)
            if len(remetente_mensagem) > 1:
                remetente, mensagem = remetente_mensagem[0], remetente_mensagem[1]
            else:
                remetente, mensagem = remetente_mensagem[0], ""
            dados.append([data, hora, remetente, mensagem])

    df = pd.DataFrame(dados, columns=['data', 'hora', 'remetente', 'mensagem'])
    return df

# Função para resumo das conversas
def resumo_conversas(df):
    resumo = df['remetente'].value_counts().reset_index()
    resumo.columns = ['remetente', 'total_conversas']
    resumo = resumo.sort_values(by='total_conversas', ascending=False)
    return resumo

# Função para gráfico de pizza
def grafico_pizza(df):
    resumo = df['remetente'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(resumo, labels=resumo.index, autopct='%1.1f%%', startangle=90)
    plt.title('Percentual de Mensagens por Remetente')
    plt.axis('equal')
    plt.show()

# Função para gráfico de linhas
def grafico_linhas(df):
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
    df_grouped = df.groupby(['data', 'remetente']).size().unstack(fill_value=0)

    plt.figure(figsize=(12, 6))
    for remetente in df_grouped.columns:
        plt.plot(df_grouped.index, df_grouped[remetente], marker='', label=remetente)

    plt.title('Quantidade de Mensagens ao Longo do Tempo')
    plt.xlabel('Data')
    plt.ylabel('Quantidade de Mensagens')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.show()

def main():
    df = ler_arquivo('Conversas.txt')

    while True:
        print("\nEscolha uma opção:")
        print("1. Resumo das conversas")
        print("2. Gráfico de pizza")
        print("3. Gráfico de linhas")
        print("4. Sair")

        opcao = input("Digite o número da opção: ")

        if opcao == '1':
            print(resumo_conversas(df))
        elif opcao == '2':
            grafico_pizza(df)
        elif opcao == '3':
            grafico_linhas(df)
        elif opcao == '4':
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()

import pandas as pd
import re
import matplotlib.pyplot as plt

# Função para ler o arquivo e criar o DataFrame
def ler_arquivo(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        linhas = file.readlines()

    dados = []
    padrao = r'(\d{2}/\d{2}/\d{4}) (\d{2}:\d{2}) - (.+)'

    for linha in linhas:
        match = re.match(padrao, linha)
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
    resumo.columns = ['remetente', 'total de mensagens']
    resumo = resumo.sort_values(by='total de mensagens', ascending=False)
    return resumo

def historico_remetente(df, remetente):
    historico = df[df['remetente'] == remetente]
    return historico

def grafico_remetente(df, remetente):
    historico = df[df['remetente'] == remetente].copy()
    historico['data'] = pd.to_datetime(historico['data'], dayfirst=True)
    historico_agrupado = historico.groupby(historico['data'].dt.date).count()

    plt.figure(figsize=(10, 5))
    plt.bar(historico_agrupado.index, historico_agrupado['mensagem'])
    plt.title(f'Histórico de Mensagens - {remetente}')
    plt.xlabel('Data')
    plt.ylabel('Quantidade de Mensagens')
    plt.xticks(rotation=45)
    plt.show()

def grafico_pizza(df):
    grafico = df['remetente'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(grafico, labels=grafico.index, autopct='%1.1f%%', startangle=90)
    plt.title('Mensagens por Remetente')
    plt.axis('igual')
    plt.show()

def grafico_linhas(df):
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
    df_agrupado = df.groupby(['data', 'remetente']).size().unstack(fill_value=0)

    plt.figure(figsize=(12, 6))
    for remetente in df_agrupado.columns:
        plt.plot(df_agrupado.index, df_agrupado[remetente], marker='', label=remetente)

    plt.title('Mensagens ao Longo do Tempo')
    plt.xlabel('Data')
    plt.ylabel('Mensagens')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.show()

def main():
    df = ler_arquivo('Conversas.txt')

    while True:
        print("\nEscolha uma opção:")
        print("1. Numero de conversas")
        print("2. Historico do remetente")
        print("3. Gráfico do Historico do remetente")
        print("4. Gráfico de pizza")
        print("5. Gráfico de linhas")
        print("6. Sair")

        opcao = input("Digite o número da opção: ")

        if opcao == '1':
            print(resumo_conversas(df))
        elif opcao == '2':
            remetente = input("Digite o nome do remetente: ")
            print(historico_remetente(df, remetente))
        elif opcao == '3':
            remetente = input("Digite o nome do remetente: ")
            grafico_remetente(df, remetente)
        elif opcao == '4':
            grafico_pizza(df)
        elif opcao == '5':
            grafico_linhas(df)
        elif opcao == '6':
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()

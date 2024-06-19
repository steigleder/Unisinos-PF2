#-----Script utilizado para extração de dados financeiros do portal Yahoo Finanças
#-----
#-----Utilização:
#-----1.informar o código de negociação da ação na B3, acrescentando o final ".SA"
#-----2.informar o período desejado

import yfinance as yf
from datetime import datetime

#----- tratamento do preço da ação
def get_stock_prices(ticker, start_date, end_date):
    try:

        #----- seleciona o código e o período desejado
        stock_data = yf.download(ticker, start=start_date, end=end_date)

        #----- seleciona o preço de fechamento
        stock_prices = stock_data['Close']

        return stock_prices
    except Exception as e:
        return f"Erro ao obter os valores da ação: {str(e)}"


#----- tratamento ds valores do IBOV
def get_ibov_prices(start_date, end_date):
    try:
        #----- seleciona o código do IBOV e o período desejado
        ibov_data = yf.download('^BVSP', start=start_date, end=end_date)

        # ----- seleciona o código do IBOV e o período desejado
        ibov_prices = ibov_data['Close']

        return ibov_prices
    except Exception as e:
        return f"Erro ao obter os valores do índice IBOV: {str(e)}"


if __name__ == "__main__":
    # Solicitar o código de negociação e a data inicial
    ticker = input("Informar a ação no formato ABCD3.SA: ")
    start_date_str = input("Informar a data inicial no formato AAAA-MM-DD: ")

    # Converter a data inicial para o formato datetime
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')

    # Calcular a data final
    end_date = datetime.today()

    # Obter os valores da ação para o intervalo especificado
    stock_prices = get_stock_prices(ticker, start_date, end_date)

    # Obter os valores do índice IBOV para o intervalo especificado
    ibov_prices = get_ibov_prices(start_date, end_date)

    # Calcular o preço de fechamento da data inicial
    start_stock_price = stock_prices.iloc[0]
    start_ibov_price = ibov_prices.iloc[0]

    # Calcular a diferença percentual para cada data em relação à data inicial
    stock_percent_diff = ((stock_prices - start_stock_price) / start_stock_price * 100).reset_index()
    ibov_percent_diff = ((ibov_prices - start_ibov_price) / start_ibov_price * 100).reset_index()

    # Exibir as diferenças percentuais para cada data
    print(f"Listagem referente a data inicial ({start_date.strftime('%Y-%m-%d')}):\n")
    print(f"Ticket;Data;Valor do Ticket;Valor do IBOV")
    for i in range(len(stock_percent_diff)):
        date = stock_percent_diff.iloc[i]['Date']
        stock_diff = stock_percent_diff.iloc[i]['Close']
        ibov_diff = ibov_percent_diff.iloc[i]['Close']
        print(f"{ticker};{date.strftime('%d/%m/%Y')};{stock_prices[date]};{ibov_prices[date]}")

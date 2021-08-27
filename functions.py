# Autor Leonardo Dourado
# É proibida a utilização do programa ou cópia de parte do código sem a autorização do autor.

import requests
import time

def get_count_cryptocurrencies(category):
    '''Essa função retorna a quantidade de
     moedas disponíveis.'''

    if category == "spot":
        URL_query = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&category=spot"
        r = requests.get(url = URL_query)
        data_count_crypto = r.json()
    elif category == "futures":
        URL_query = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&category=futures"
        r = requests.get(url = URL_query)
        data_count_crypto = r.json()

    return int(data_count_crypto['data']['totalCount'])

def get_all_cryptocurrencies_spot(limit=get_count_cryptocurrencies("spot")):
    '''Essa função retorna as estatísticas das moedas no mercado spot.'''
    limit = get_count_cryptocurrencies("spot")
    URL_query = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit={0}&sortBy=market_cap&category=spot&sortType=desc&convert=USD,BTC,ETH&cryptoType=all&tagType=all&audited=false&aux=ath,atl,high24h,low24h,num_market_pairs,cmc_rank,date_added,tags,platform,max_supply,circulating_supply,total_supply,volume_7d,volume_30d".format(limit)
    r = requests.get(url = URL_query)
    data_all_cryptocurrencies = r.json()

    return data_all_cryptocurrencies

def get_all_cryptocurrencies_future(limit=get_count_cryptocurrencies("futures")):
    '''Essa função retorna as estatísticas das moedas no mercado future.'''
    limit = get_count_cryptocurrencies("futures")
    URL_query = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit={0}&sortBy=market_cap&category=futures&sortType=desc&convert=USD,BTC,ETH&cryptoType=all&tagType=all&audited=false&aux=ath,atl,high24h,low24h,num_market_pairs,cmc_rank,date_added,tags,platform,max_supply,circulating_supply,total_supply,volume_7d,volume_30d".format(limit)
    r = requests.get(url = URL_query)
    data_all_cryptocurrencies = r.json()

    return data_all_cryptocurrencies

def get_coins_by_exchange(exchange_slug):
    '''Essa função retorna todas as moedas de uma exchange específica e salva em arquivo.'''
    coins_set = set()
    for page in range(0,100):
        URL_query = "https://api.coingecko.com/api/v3/exchanges/{0}/tickers?page={1}".format(exchange_slug, page)
        r = requests.get(url = URL_query)
        data_exchange = r.json()

        if len(data_exchange['tickers']) > 0:
            for i in range(0,len(data_exchange['tickers'])):
                coins_set.add(data_exchange['tickers'][i]['base'])
        else:
            break

    try:
        file = open("coins_by_exchange.bin","w")
        for line in coins_set:
            file.write("{0}\n".format(line))
        file.close()
    except Exception as ex:
        print(ex)

    return list(coins_set)

def get_coins_list():
    '''Essa função retorna de um arquivo uma lista com as moedas armazenadas.'''
    coins_list = list()
    try:
        file = open("coins_by_exchange.bin","r")
        
        for line in file:
            coins_list.append(line.replace("\n",""))

        file.close()
    except Exception as ex:
        print(ex)

    return coins_list

#def get_exchanges_by_cryptocurrency(coin_slug):
#    '''Essa função retorna em quais exchanges uma determinada moeda está listada.'''
#    exchanges_set = set()
#    URL_query = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/market-pairs/latest?slug={0}".format(coin_slug)
#    r = requests.get(url = URL_query)
#    data_exchanges = r.json()
#    exchanges_array_size = len(data_exchanges['data']['marketPairs'])

#    for i in range(1,exchanges_array_size):
#        exchanges_set.add(data_exchanges['data']['marketPairs'][i]['exchangeSlug'])

#    return exchanges_set

def check_crypto_in_exchange(coin_symbol, exchange_coins_list):
    '''Essa função retorna True se uma moeda está listada em uma exchange específica e False se não está listada.'''
    if coin_symbol in exchange_coins_list:
        return True
    else:
        return False

def get_top_gain(top_n, marketcap_greater, volume24h, exchanges, window):
    '''Essa função atualiza os campos da janela com o top n de altas de moedas listada em ordem decrescente.'''
    cryptocurrencies = list()
    data = get_all_cryptocurrencies_spot()
    top_return = list()

    exchanges_coin_list = get_coins_list()

    for i in range(0, int(get_count_cryptocurrencies("spot"))):
        if float(data['data']['cryptoCurrencyList'][int(i)]['quotes'][2]['marketCap']) < marketcap_greater and volume24h > float(data['data']['cryptoCurrencyList'][int(i)]['quotes'][2]['volume24h']):
            continue
        cryptocurrencies.append({'name': data['data']['cryptoCurrencyList'][int(i)]['name'], 'slug': data['data']['cryptoCurrencyList'][int(i)]['slug'], 'symbol': data['data']['cryptoCurrencyList'][int(i)]['symbol'], 'Variação 1h': data['data']['cryptoCurrencyList'][int(i)]['quotes'][2]['percentChange1h'], 'Variação 24h': data['data']['cryptoCurrencyList'][int(i)]['quotes'][2]['percentChange24h']})

    cryptocurrencies_sorted = sorted(cryptocurrencies, key=lambda k: k['Variação 1h'], reverse=True)

    counter = 0

    for cryptocurrency in cryptocurrencies_sorted:
        if check_crypto_in_exchange(cryptocurrency['symbol'], exchanges_coin_list):
            index = str(counter+1)
            #print(".{0}.".format(cryptocurrency['symbol']))
            window.Element("top_gain_{0}_1".format(index)).Update(cryptocurrency['name'])
            window.Element("top_gain_{0}_2".format(index)).Update(cryptocurrency['slug'])
            window.Element("top_gain_{0}_3".format(index)).Update(cryptocurrency['symbol'])
            window.Element("top_gain_{0}_4".format(index)).Update("{0:.2f}".format(cryptocurrency['Variação 1h']))
            counter += 1
        
        if counter == top_n:
                break
            
def get_top_loss(top_n, marketcap_greater, volume24h, exchanges, window):
    '''Essa função atualiza os campos da janela com o top n de baixas de moedas listada em ordem crescente.'''
    cryptocurrencies = list()
    data = get_all_cryptocurrencies_future()
    top_return = list()

    exchange_coin_list = get_coins_list()

    for i in range(0, int(get_count_cryptocurrencies("futures"))):
        if float(data['data']['cryptoCurrencyList'][int(i)]['quotes'][2]['marketCap']) < marketcap_greater and volume24h > float(data['data']['cryptoCurrencyList'][int(i)]['quotes'][2]['volume24h']):
            continue
        cryptocurrencies.append({'name': data['data']['cryptoCurrencyList'][int(i)]['name'], 'slug': data['data']['cryptoCurrencyList'][int(i)]['slug'], 'symbol': data['data']['cryptoCurrencyList'][int(i)]['symbol'], 'Variação 1h': data['data']['cryptoCurrencyList'][int(i)]['quotes'][2]['percentChange1h'], 'Variação 24h': data['data']['cryptoCurrencyList'][int(i)]['quotes'][2]['percentChange24h']})

    cryptocurrencies_sorted = sorted(cryptocurrencies, key=lambda k: k['Variação 1h'])

    counter = 0

    for cryptocurrency in cryptocurrencies_sorted:
        if check_crypto_in_exchange(cryptocurrency['symbol'], exchange_coin_list):
            index = str(counter+1)
            #print(".{0}.".format(cryptocurrency['symbol']))
            window.Element("top_loss_{0}_1".format(index)).Update(cryptocurrency['name'])
            window.Element("top_loss_{0}_2".format(index)).Update(cryptocurrency['slug'])
            window.Element("top_loss_{0}_3".format(index)).Update(cryptocurrency['symbol'])
            window.Element("top_loss_{0}_4".format(index)).Update("{0:.2f}".format(cryptocurrency['Variação 1h']))
            counter += 1

        if counter == top_n:
            break

def repeat_by_time_top_gain(top_n, marketcap_greater, volume24h, exchanges, window):
    '''Essa função executa em loop temporal a função get_top_gain.'''
    while True:
        get_top_gain(top_n, marketcap_greater, volume24h, exchanges, window)
        time.sleep(int(returnConfigFile()[3]))

def repeat_by_time_top_loss(top_n, marketcap_greater, volume24h, exchanges, window):
    '''Essa função executa em loop temporal a função get_top_loss.'''
    while True:
        get_top_loss(top_n, marketcap_greater, volume24h, exchanges, window)
        time.sleep(int(returnConfigFile()[3]))

def clear_gain_fields(top_n, window):
    '''Essa função limpa os campos de ganho das moedas na janela.'''
    for index in range(1,top_n+1):
        window.Element("top_gain_{0}_1".format(index)).Update(" ")
        window.Element("top_gain_{0}_2".format(index)).Update(" ")
        window.Element("top_gain_{0}_3".format(index)).Update(" ")
        window.Element("top_gain_{0}_4".format(index)).Update(" ")

def clear_loss_fields(top_n, window):
    '''Essa função limpa os campos de perda das moedas na janela.'''
    for index in range(1,top_n+1):
        window.Element("top_loss_{0}_1".format(index)).Update(" ")
        window.Element("top_loss_{0}_2".format(index)).Update(" ")
        window.Element("top_loss_{0}_3".format(index)).Update(" ")
        window.Element("top_loss_{0}_4".format(index)).Update(" ")

def getValue(config_line):
    '''Essa função separa o parâmetro do valor atribuído, retornando apenas o valor atribuído.'''
    value = config_line.split("=")
    return value[1]

def loadConfigFile(window):
    '''Essa função carrega nos campos da interface GUI os parâmetros salvos no arquivo.'''
    try:
        file = open("config.bin","r")
        counter = 1
        for line in file:
            window.Element(counter).Update(getValue(line))
            counter += 1
        file.close()
    except FileNotFoundError:
        return False

def saveParametersInFile(top_currencies,marketcap_greater,volume24h,time_refresh_seconds):
    '''Essa função salva os parâmetros no arquivo de configuração.'''
    try:
        file = open("config.bin","w")
        file.write("top_currencies={0}\n".format(top_currencies.replace("\n","")))
        file.write("marketcap_greater={0}\n".format(marketcap_greater.replace("\n","")))
        file.write("volume24h={0}\n".format(volume24h.replace("\n","")))
        file.write("time_refresh_seconds={0}\n".format(time_refresh_seconds.replace("\n","")))
        file.close()
    except Exception as ex:
        print(ex)

def returnConfigFile():
    ''' Essa função retorna os parâmetros definidos e salvos no arquivo de configuração.'''
    try:
        file = open("config.bin","r")
        config_parameters = list()
        counter = 1
        for line in file:
            line_return = getValue(line)
            line_return = line_return.replace("\n","")
            config_parameters.append(line_return)
            counter += 1
        file.close()
        return config_parameters
    except FileNotFoundError:
        return [None,None,None,None]

#get_coins_by_exchange("binance")

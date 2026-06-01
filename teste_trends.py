from pytrends.request import TrendReq

pytrends = TrendReq(hl='pt-BR', tz=360)

termos = ['Python', 'Inteligência Artificial', 'AWS', 'Databricks']

pytrends.build_payload(termos, timeframe='today 12-m', geo='BR')

df = pytrends.interest_over_time()

print("Deu certo! Aqui estão os dados:")
print(df.tail())
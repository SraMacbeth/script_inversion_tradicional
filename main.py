import yfinance
import pandas

def download_dataframe(ticker, initial_date, final_date):

    dataframe = yfinance.download(ticker, initial_date, final_date)

    return dataframe

df = download_dataframe("TSLA", "2000-01-01", "2026-05-17")

#print(df)

# Primeras 5 filas del dataframe
#print(df.head())

# Tipos de datos de la columnas y, si hay, valores nulos
#print(df.info())

# Index del dataframe
#print(df.index)

# Nueva columna que calcula la variacion del precio de cierre de cada dia
df['Rendimiento_Diario'] = df['Close'].pct_change()

# Primeras 5 filas del dataframe
print(df.head())
# Ultimas 5 filas del dataframe
print(df.tail())
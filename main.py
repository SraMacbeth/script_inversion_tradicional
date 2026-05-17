import yfinance
import pandas
import numpy as np

# —------------ BACKTESTING-----------------------------------------------

# Conexión a internet y descarga de datos históricos reales
def download_dataframe(ticker, initial_date, final_date):

    dataframe = yfinance.download(ticker, initial_date, final_date)

    return dataframe

df = download_dataframe("TSLA", "2000-01-01", "2026-05-17")
#print(df)

# Limpieza y estructuración de los datos en un DataFrame con índice de fechas

# Primeras 5 filas del dataframe
#print(df.head())

# Tipos de datos de la columnas y, si hay, valores nulos
#print(df.info())

# Index del dataframe
#print(df.index)

# Cálculo de las variaciones de precio diarias
# Nueva columna que calcula la variacion del precio de cierre de cada dia
df['Rendimiento_Diario'] = df['Close'].pct_change()

'''
Aplicación de Estrategia "El cruce de Medias Móviles (Moving Averages)"

Media Móvil: promedio del precio de cierre de los últimos N días.

Media de corto plazo (ej: 20 días): la línea reacciona rápido a los movimientos recientes del precio.

Media de largo plazo (ej: 50 días): la línea será mucho más suave y mostrará la tendencia general del año. 

Regla:

Señal de COMPRA: cuando la línea de corto plazo cruza hacia arriba a la de largo plazo.Significa que el precio está en alza.

Señal de VENTA: cuando la línea de corto plazo cruza hacia abajo a la de largo plazo.Significa que el precio está en baja.
'''

# Alisado de precios con promedios móviles de 20 y 50 días.
# Se crean las nuevas columnas que representan las medias móviles
# df["Close"] --> columna sobre la que se aplican las operaciones. Se usa el precio de cierre para evaluar la tendencia real del día. En Pandas esto es una serie, una columna suelta.
# .rolling(window=20) --> cantidad de filas (días) sobre las que se aplican las operaciones. En Pandas esto es una Ventana Móvil (Rolling Window). Para cada fila se toma una ventana desfasada por un día.
# .mean() --> operación a aplicar: promedio. Reduce los valores de la ventana a un único número que se guarda en la nueva columna.
df["Media_Corta"] = df["Close"].rolling(window=20).mean()
df["Media_Larga"] = df["Close"].rolling(window=50).mean()

# Se decide si el mercado está en alza o la baja. 
# Se crea la columna Posición que indica el estado del comprador respecto de la acción evaluada.
# Puede tomar dos valores: 
# Long: Significa que se compró la acción esperando que su precio suba en el futuro para venderla más cara y ganar la diferencia. Se representa con un 1.
# Neutral: Significa que no se tiene ninguna acción de esa empresa. Se representa con un 0.
df["Posicion"] = np.where(df["Media_Corta"] > df["Media_Larga"], 1 , 0) 

# Se encuentran los días exactos donde hay que comprar o vender
# Se crea la columna Signal (Señal) que indicará al usuario si es momentos d comprar, vender o esperar.Se calcula comparando la posicion del día actual con el día anterior. 
# Usa la formula posicion_actual - posicion_anterior = señal
# Puede tomar 3 valores, según los resultados de la ecuación
# 1 - 0 = 1 (hoy long - ayer neutral = Comprar!)
# 1 - 1 = 0 (hoy long - ayer long = Ya esta comprado. Esperar.)
# 0 - 1 = -1 (hoy nuetral - ayer long = la tendencia se rompió. Vender!)
df['Signal'] = df['Posicion'].diff()

# Primeras 5 filas del dataframe
print(df.head())
# Ultimas 5 filas del dataframe
print(df.tail())
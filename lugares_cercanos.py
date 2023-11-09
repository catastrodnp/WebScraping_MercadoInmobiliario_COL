import pandas as pd
import numpy as np

def lugares_cercanos(col):
  lugares = ['polic', 'hospital', 'centro comercial', 'restaurante','colegio',
                     'universidad','banco','supermercado','parque','transmilenio','cajero',
                     'iglesia','cicloruta','lavander']

  # Iterar a través de las palabras/frases y crear columnas
  for lugar in lugares:
      df[lugar] = np.where(df[col].str.contains(lugar, case=False), 1, 0)
  
  return df

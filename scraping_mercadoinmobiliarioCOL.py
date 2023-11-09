import requests
from bs4 import BeautifulSoup
import pandas as pd
import warnings

import json
warnings.simplefilter(action='ignore', category=FutureWarning)

def data_mitula(mun,pags):

  df_full=pd.DataFrame()

  titulos = []
  descripciones = []
  precios = []
  areas = []
  num_banos = []
  num_habitaciones = []
  ubicaciones = []
  fechas_publicacion = []
  facilities_list = []


  for pag in range(1,pags):
    url=f'https://casas.mitula.com.co/searchRE/orden-0/op-1/q-{mun}/pag-{pag}?req_sgmt=REVTS1RPUDtVU0VSX1NFQVJDSDtTRVJQOw=='


    response = requests.get(url)
    print(response)
    soup = BeautifulSoup(response.text, "html.parser")

    viviendas = soup.find_all('div', {'class': 'listing-card'})


    print(len(viviendas))
    #print(viviendas)
    # Iterar a través de las viviendas
    for vivienda in viviendas:
      try:
        #print(vivienda)
        titulo = vivienda.find('div', {'class': 'listing-card__title'}).text.strip()
        precio = vivienda.find('div', {'class': 'price'}).text.strip()
        #print(precio)
        area = vivienda.find('div', {'class': 'card-icon__area'}).find_next('span').text.strip()
        bano = str(vivienda.find('span', {'data-test': 'bathrooms'})).split('data-test="bathrooms">')[-1].replace('</span>','')
        hab = str(vivienda.find('span', {'data-test': 'bedrooms'})).split('data-test="bedrooms">')[-1].replace('</span>','')
        ubicacion = vivienda.find('div', {'class': 'listing-card__location'}).text.strip()
        fecha_publicacion = vivienda.find('span', {'class': 'published-date'}).text.strip()
        facilities = sorted(list(set([item.text.strip() for item in vivienda.find_all('span', {'class': 'facility-item__text'})])))
        #print(titulo,precio,area,bano)


        titulos.append(titulo)
        precios.append(precio)
        areas.append(area)
        num_banos.append(bano)
        num_habitaciones.append(hab)
        ubicaciones.append(ubicacion)
        fechas_publicacion.append(fecha_publicacion)
        facilities_list.append(facilities)

        data = {'Título': titulos,
                'Precio': precios,
                'Área (m²)': areas,
                'Número de Baños': num_banos,
                'Número de Habitaciones': num_habitaciones,
                'Ubicación': ubicaciones,
                'Fecha de Publicación': fechas_publicacion,
                'Facilities': facilities_list
                }

        df=pd.DataFrame(data)
        #display(df)
        df_full=df_full.append(df,ignore_index=True)

        
        df_full['Facilities']=df_full['Facilities'].astype(str).str.replace("'","").str.replace("[","").str.replace("]","").str.replace(" ,",",").str.replace(", ",",")
        # Dividir la columna 'amenities' en elementos individuales y crear columnas correspondientes
        facilities_columns = df_full['Facilities'].str.get_dummies(',')        
        
        # Concatenar las nuevas columnas al DataFrame original
        df_full = pd.concat([df_full, facilities_columns], axis=1)

        #df_full = df_full.loc[:, ~df_full.columns.duplicated()]
        
        # Reemplazar NaN con 0 en las nuevas columnas
        df_full = df_full.fillna(0)
      

      except:
        pass

  return df_full

def data_mitula_geo(mun,pag):
  url=f'https://casas.mitula.com.co/searchRE/orden-0/op-1/q-{mun}/pag-{pag}?req_sgmt=REVTS1RPUDtVU0VSX1NFQVJDSDtTRVJQOw=='

  response = requests.get(url)
  #print(response)
  soup = BeautifulSoup(response.text, "html.parser")
  viviendas = soup.find_all('div', {'class': 'listing-card'})

  script_tag = soup.find('script', type='application/ld+json')
  json_data = json.loads(script_tag.string)

  precios=[]
  lats=[]
  longs=[]
  names=[]
  descs=[]
  beds=[]
  baths=[]
  dptos=[]
  muns=[]
  calles=[]
  areas=[]


  for i,vivienda in enumerate(viviendas):
    try:
      #print(i)
      precio = vivienda.find('div', {'class': 'price'}).text.strip()

      latitude = json_data['about'][i]['geo']['latitude']
      longitude = json_data['about'][i]['geo']['longitude']
      name=json_data['about'][i]['name']
      desc=json_data['about'][i]['description']
      precios.append(precio)
      lats.append(latitude)
      longs.append(longitude)
      names.append(name)
      descs.append(desc)

      #ROOMS
      bed=json_data['about'][i]['numberOfBedrooms']
      bath=json_data['about'][i]['numberOfBathroomsTotal']
      beds.append(bed)
      baths.append(bath)


      #ADDRESS
      dpto=json_data['about'][i]['address']['addressRegion']
      mun=json_data['about'][i]['address']['addressLocality']
      calle=json_data['about'][i]['address']['streetAddress']
      dptos.append(dpto)
      muns.append(mun)
      calles.append(calle)

      #AREA
      area=json_data['about'][i]['floorSize']['value']
      areas.append(area)

    except:
      pass

  data={'precio':precios,'latitud':lats,'longitud':longs,'nombre':names,'descripcion':descs,
        #'cuarto':beds,'bano':baths,
        #'depto':dptos,
        #'mun':muns,#'calle':calles,
        #'area':areas
        }
  df=pd.DataFrame(data)

  return df

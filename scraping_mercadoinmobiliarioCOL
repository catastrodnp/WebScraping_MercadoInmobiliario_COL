

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

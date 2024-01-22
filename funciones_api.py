import pandas as pd

# lectura de datasets

df_plf = pd.read_parquet('Datasets/parquet/API/Surprise/df_plf.parquet')
df_plf1 = pd.DataFrame(df_plf.groupby(['genres','release_year'])['playtime_forever'].sum().sort_values(ascending=False))
df_plu2 = pd.DataFrame(df_plf.groupby(['genres','user_id'])['playtime_forever'].sum().sort_values(ascending=False))
df_feel = pd.read_parquet('Datasets/parquet/API/feel.parquet')
lista_generos = list(df_plf1.droplevel(1).index.sort_values().unique())
lista_anios = list(df_feel.release_year.sort_values().unique())
lista_empresa = list(df_feel.developer.unique())

df_usuarios = pd.read_parquet('Datasets/parquet/Recomendacion/Surprise/df_usuarios.parquet')
df_titles = pd.read_parquet('Datasets/parquet/Recomendacion/Surprise/df_titles.parquet')

def presentacion(): # estructura html de la pagina de inicio
    return '''
    <html>
        <head>
            <title>API Steam</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                p {
                    color: #666;
                    text-align: center;
                    font-size: 18px;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <h1>API de consultas de videojuegos de la plataforma Steam</h1>
            <p>Bienvenido a la API de Steam donde se pueden hacer diferentes consultas sobre la plataforma de videojuegos.</p>
            <p>INSTRUCCIONES:</p>
            <p>Escriba <span style="background-color: lightgray;">/docs</span> a continuación de la URL actual de esta página para interactuar con la API</p>
        </body>
    </html>
    '''

def PlayTimeGenre(genre):
    if genre not in lista_generos:
        return 'El genero elegido no es valido'
    anio = df_plf1.loc[genre].index[0]
    dic = {f"Año de lanzamiento con más horas jugadas para Género {genre}": str(anio)}
    return dic

def UserForGenre(genre):
    if genre not in lista_generos:
        return 'El genero elegido no es valido'
    user = df_plu2.loc[genre].index[0]
    df_plu = df_plf.loc[genre,:,user].groupby(['release_year'])['playtime_forever'].sum().sort_index(ascending=False)
    dic = {f'Usuario con más horas jugadas para Género {genre}':user}
    lista = []
    for index,value in df_plu.items():
        if value == 0:
            continue
        lista.append({f'Año: {index}':f'Horas: {round(value/60,0)}'})
    dic.update({'Horas jugadas':lista})
    return dic

def UsersRecommend(year):
    try:
        year = int(year)
    except:
        return 'No se ingreso un anio valido'
    if year not in lista_anios:
        return 'No se ingreso un anio valido'
    df_ur = df_feel[(df_feel['release_year']==year) & (df_feel['recommend']==True)&(df_feel['sentiment_analysis']>0)].groupby(['app_name'])['item_id'].sum().sort_values(ascending=False)
    lista = []
    for i in range(1,4):
        lista.append({f'Puesto {i}':df_ur.index[i]})
    return lista

def UsersWorstDeveloper(year):
    try:
        year = int(year)
    except:
        return 'No se ingreso un anio valido'
    if year not in lista_anios:
        return 'No se ingreso un anio valido'
    df_uw = df_feel[(df_feel['release_year']==year) & (df_feel['recommend']==False)&(df_feel['sentiment_analysis']==0)].groupby(['developer'])['item_id'].sum().sort_values(ascending=False)
    lista = []
    for i in range(1,4):
        lista.append({f'Puesto {i}':df_uw.index[i]})
    return lista

def sentiment_analysis(empresa):
    if empresa not in lista_empresa:
        return 'La empresa desarrolladora seleccionada no es valida'
    df_sa = df_feel[(df_feel['developer']==empresa)].groupby(['sentiment_analysis'])['item_id'].sum().sort_index()
    lista = [f'Negative: {df_sa.iloc[0]}',f'Neutral: {df_sa.iloc[1]}',f'Positive: {df_sa.iloc[2]}']
    dic = {empresa:lista}
    return dic

def recomendacion_juego(item_id):
    try:
        result = df_titles[df_titles['itemID'] == item_id].ItemRecomendations.values[0]
        resultado = []
        count = 1
        for i in result:
            resultado.append({'Puesto':count,'ID':i,'Nombre':df_titles[df_titles['itemID'] == i].itemName.values[0]})
            count +=1
        return resultado
    except:
        return print(f'Sin informacion disponible para el juego {item_id}')

def recomendacion_usuario(user_id):
    try:
        result = df_usuarios[df_usuarios['userID'] == user_id].userRecomendation.values[0]
        resultado = []
        count = 1
        for i in result:
            resultado.append({'Puesto':count,'ID':i,'Nombre':df_titles[df_titles['itemID'] == i].itemName.values[0]})
            count +=1
        return resultado
    except:
        return print(f'Sin informacion disponible para el usuario {user_id}')

import pandas as pd
import operator

df_playtime = pd.read_parquet('../Datasets/parquet/API/playtime_red.parquet')
df_feel = pd.read_parquet('../Datasets/parquet/API/feel.parquet')
lista_generos = list(df_playtime.genres.sort_values().unique())
lista_anios = list(df_feel.release_year.sort_values().unique())
lista_empresa = list(df_feel.developer.unique())

user_rating_sim_df = pd.read_parquet('../Datasets/parquet/Recomendacion/Final/user_rating_sim_df_red.parquet')
user_ratings_matrix = pd.read_parquet('../Datasets/parquet/Recomendacion/Final/user_ratings_matrix_red.parquet')
diccionario_juegos = pd.read_parquet('../Datasets/parquet/Recomendacion/Final/diccionario_juegos_red.parquet')
item_sim_df = pd.read_parquet('../Datasets/parquet/Recomendacion/Final/item_sim_df_red.parquet')

def presentacion():
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
    df_plf = df_playtime[df_playtime['genres'] == genre].groupby(['release_year'])['playtime_forever'].sum().sort_values(ascending=False)
    anio = df_plf.index[0]
    dic = {f"Año de lanzamiento con más horas jugadas para Género {genre}": anio}
    return dic

def UserForGenre(genre):
    if genre not in lista_generos:
        return 'El genero elegido no es valido'
    df_plut = df_playtime[df_playtime['genres']==genre].groupby(['user_id'])['playtime_forever'].sum().sort_values(ascending=False)
    user = df_plut.index[0]
    df_plu = df_playtime[(df_playtime['genres']==genre) & (df_playtime['user_id']==user)].groupby(['release_year'])['playtime_forever'].sum().sort_index(ascending=False)
    dic = {f'Usuario con más horas jugadas para Género {genre}':user}
    lista = []
    for index,value in df_plu.items():
        if value == 0:
            continue
        lista.append({f'Año: {index}':f'Horas: {value/60}'})
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
        item_name = diccionario_juegos[diccionario_juegos.item_id==item_id].item_name.values[0]
    except:
        return print(f'Sin informacion disponible para el juego {item_id}')
    count = 1
    string = f'Los Juegos similares a ID juego {item_id}, nombre {item_name} son:\n'
    for item in item_sim_df.sort_values(by = item_name, ascending = False).index[1:6]:
        string += f'No. {count}: ID {diccionario_juegos[diccionario_juegos.item_name==item].item_id.values[0]}, nombre {item}'
        count +=1
    return string

def recomendacion_usuario(user_id):
    similarity_constant = 0.7
    if user_id not in user_rating_sim_df.columns:
        return(f'Sin informacion disponible para ese usuario {user_id}')
    
    sim_users = user_rating_sim_df[user_rating_sim_df>similarity_constant].sort_values(by=user_id, ascending=False)

    best = []
    most_common = {}

    for i in sim_users:
        user_scores = user_ratings_matrix.loc[:, i]
        max_scores = user_scores[user_scores>similarity_constant]
        for j in max_scores:
            best.append(user_ratings_matrix[user_ratings_matrix.loc[:, i]==j].index.tolist())
        
    for i in range(len(best)):
        for j in best[i]:
            if j in most_common:
                most_common[j] += 1
            else:
                most_common[j] = 1
    
    sorted_list = sorted(most_common.items(), key=operator.itemgetter(1), reverse=True)
    
    lista = []
    count = 1
    for i in sorted_list[:5]:
        lista.append({'Puesto':str(count),'ID':str(diccionario_juegos[diccionario_juegos.item_name==i[0]].item_id.values[0]),'Nombre':str(i[0])})
        count +=1
    return lista
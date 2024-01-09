# Importaciones
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import funciones_api as fp

import importlib
importlib.reload(fp)

# Se instancia la aplicación
app = FastAPI()

# Funciones

# funcion de response
@app.get(path="/", 
         response_class=HTMLResponse,
         tags=["Home"])
def home():
    '''
    Página de inicio que muestra una presentación.

    Returns:
    HTMLResponse: Respuesta HTML que muestra la presentación.
    '''
    return fp.presentacion()

# funcion PlayTimeGenre
@app.get(path = '/PlayTimeGenre',
          description = """ <font color="blue">
                        INSTRUCCIONES<br>
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el genero en el box abajo.<br>
                        3. Scrollear a "Resposes" para ver el año de lanzamiento con mas horas jugadas para ese genero.
                        </font>
                        """,
         tags=["Consultas Generales"])
def PlayTimeGenre(genre: str = Query(..., 
                                description="Genero", 
                                example="Action")):
        
    return fp.PlayTimeGenre(genre)
    
# funcion UserForGenre
@app.get(path = '/UserForGenre',
          description = """ <font color="blue">
                        INSTRUCCIONES<br>
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el genero en el box abajo.<br>
                        3. Scrollear a "Resposes" para ver el usuario con mas horas jugadas para dicho genero.
                        </font>
                        """,
         tags=["Consultas Generales"])
def UserForGenre(genre: str = Query(..., 
                                description="Genero", 
                                example='Action')):
    return fp.UserForGenre(genre)

# funcion UsersRecommend
@app.get(path = '/UsersRecommend',
          description = """ <font color="blue">
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el anio en formato YYYY.<br>
                        3. Scrollear a "Resposes" para ver los 3 juegos mas recomendados para el anio dado.
                        </font>
                        """,
         tags=["Consultas Generales"])
def UsersRecommend(year: str = Query(..., 
                            description="Anio (formato YYYY)", 
                            example='2016')):
    return fp.UsersRecommend(year)

# funcion UserWorstDeveloper
@app.get(path = '/UsersWorstDeveloper',
          description = """ <font color="blue">
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el anio en formato YYYY.<br>
                        3. Scrollear a "Resposes" para ver Top 3 desarrolladoras con juegos MENOS recomendados por usuarios para el año dado.
                        </font>
                        """,
         tags=["Consultas Generales"])
def UsersWorstDeveloper(year: str = Query(..., 
                            description="Anio (formato YYYY)", 
                            example='2016')):
    return fp.UsersWorstDeveloper(year)

# funcion sentiment_analysis
@app.get(path = '/sentiment_analysis',
          description = """ <font color="blue">
                        1. Haga clik en "Try it out".<br>
                        2. Ingrese el nombre del desarrollador en el box abajo.<br>
                        3. Scrollear a "Resposes" para ver la cantidad resenas clasificadas en Negativas, Neutrales y Positivas para dicha desarrolladora.
                        </font>
                        """,
         tags=["Consultas Generales"])
def sentiment_analysis(empresa: str = Query(..., 
                            description="Desarrollador del videojuego", 
                            example='Valve')):
    return fp.sentiment_analysis(empresa)

# funcion recomendacion_juego
@app.get('/recomendacion_juego',
         description=""" <font color="blue">
                    INSTRUCCIONES<br>
                    1. Haga clik en "Try it out".<br>
                    2. Ingrese el id de un juego en box abajo.<br>
                    3. Scrollear a "Resposes" para ver los juegos recomendados.
                    </font>
                    """,
         tags=["Recomendación"])
def recomendacion_juego(item_id: int = Query(..., 
                                         description="ID del juego a partir del cuál se hace la recomendación de otros juego", 
                                         example=1250)):
    return fp.recomendacion_juego(item_id)

# funcion recomendacion_usuario
@app.get('/recomendacion_usuario',
         description=""" <font color="blue">
                    INSTRUCCIONES<br>
                    1. Haga clik en "Try it out".<br>
                    2. Ingrese el id del usuario en box abajo.<br>
                    3. Scrollear a "Resposes" para ver los juegos recomendados para ese usuario.
                    </font>
                    """,
         tags=["Recomendación"])
def recomendacion_usuario(user_id: str = Query(..., 
                                         description="Usuario a partir del cuál se hace la recomendación de los juego", 
                                         example="-2SV-vuLB-Kg")):
    return fp.recomendacion_usuario(user_id) 
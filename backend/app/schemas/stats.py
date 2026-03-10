from pydantic import BaseModel

class StatsSchema(BaseModel):  #Herencia de BaseModel, se crea un schema para estadisticas
    firmStats: dict  #Diccionario que contiene estadisticas de la firma
    userStats: dict  #Diccionario que contiene estadisticas del usuario

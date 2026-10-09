import csv
from pathlib import Path
from site import ENABLE_USER_SITE
import joblib
from .contracts import Entrada, Salida


def leer_csv(ruta: Path) -> list[Entrada]:

    entradas=[]
    with open(ruta) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        try:
            count=0
            for row in csv_reader:
             row1=Entrada(row)
             entradas.append(row1)
             count+=1
        except ValidationError as e:
            
            print(f"{e}")
        if count==0:
            raise ValueError 
      
    return entradas




def preprocesar(entrada: Entrada) -> list[float]:
    entrada.peso_kg=round(entrada.peso_kg,ndigits=1)
    entrada.distancia_km=round(entrada.distancia_km,ndigits=1)
    return [entrada.peso_kg, entrada.distancia_km]

def cargar_modelo(ruta: Path):
    modelo=joblib.load(ruta)
    return modelo
    
    


def predecir(entrada: Entrada, modelo) -> Salida:
    
    result_categoria=modelo.predict([entrada])
    if result_categoria=="normal":
        result_proba=modelo.predict_proba([entrada])[0][0]
    elif result_categoria=="urgente":
        result_proba=modelo.predict_proba([entrada])[0][1]
       
    return Salida(id_paquete=entrada.id_paquete, categoria=result_categoria, confianza=result_proba)


def guardar_csv(resultados: list[Salida], ruta: Path) -> None:
    
    field_names =["id_paquete","categoria", "confianza"]
    with open(ruta, mode="w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=field_names)
        escritor.writeheader()
        escritor.writerows(resultados)


def ejecutar(entrada: Path, modelo: Path, salida: Path) -> None:
    try: 
        correctas=[]
        entradas=leer_csv(entrada)
        for entr in entradas:
            entr=preprocesar(entr)
            correctas.append(entr)

        

        mod=cargar_modelo(modelo)

        for muestra in correctas:
            predecir(muestra, mod) 
    
    except ValueError as e:
        print(f"Valuerrror {e}")
    guardar_csv(muestra,salida)
        
        
if __name__ == "__main__":
    ejecutar(
        Path("data/raw/paquetes.csv"),
        Path("models/modelo.joblib"),
        Path("resultados.csv"),
    )

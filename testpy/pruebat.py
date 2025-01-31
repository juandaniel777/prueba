import requests
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
import matplotlib.pyplot as plt

# Definir la base declarativa
Base = declarative_base()

# Definir el esquema de la tabla en SQLAlchemy
class PrecioEnergia(Base):
    __tablename__ = 'precios_energia'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(String, unique=True, nullable=False)
    precio_promedio = Column(Float, nullable=False)
    precio_7d = Column(Float, nullable=False)

# Crear la conexión a SQLite
engine = create_engine("sqlite:///precios.db")
Base.metadata.create_all(engine)  # Crea la tabla si no existe

# Crear sesión
Session = sessionmaker(bind=engine)
session = Session()



#### 1 obtencion de datos

apiurl="https://l2h237eh53.execute-api.us-east-1.amazonaws.com/dev/precios"
start_date = "2024-03-15"
end_date = "2024-04-14"


def getip():
    try:
        data=requests.get(f"{apiurl}?start_date={start_date}&end_date={end_date}")
        #print(data.json())
        return data.json()
    except requests.exceptions.HTTPError as http_err:
        print(f" HTTP Error: {http_err}")
    except requests.exceptions.ConnectionError:
        print(" Error: Unable to connect to the server.")
    except requests.exceptions.Timeout:
        print(" Error: Request timed out.")
    except requests.exceptions.RequestException as err:
        print(f" Error: {err}")

            
response =getip()  

print("total dias con dats:",response['total_days'] )   

## 2 Procesamiento de los Datos
df=pd.DataFrame(response ["data"])
#print(df)

# Ejemplo de transformación
df = df.reset_index()
df = df.rename(columns={'index': 'hora'})
df_long = pd.melt(df, id_vars=['hora'], var_name='fecha', value_name='precio')

df_long['hora'] = df_long['hora'].astype(str)
df_long['hora'] = df_long['hora'].str.replace("24:00", "00:00")
df_long['timestamp'] = pd.to_datetime(df_long['fecha'] + " " + df_long['hora'], errors='coerce'  )

print(df_long)

##  3 Tratamiento de Datos Faltantes

df_long = df_long.sort_values(['timestamp'])
missing_hours = df_long[df_long['precio'].isna()]
if not missing_hours.empty:
    print(" Horas faltantes detectadas:")
    print(missing_hours[['fecha', 'hora']])  # ¿Cuáles son las horas donde hacen falta valores?

# Primero, rellenando los datos faltantes en las horas con el valor anterior más cercano disponible.
df_long['precio'] = df_long['precio'].ffill()
# Luego, para los días faltantes, se deben rellenar Luego, para los días faltantes, se deben rellenar utilizando el promedio de los 3 días previos y los 3 días posteriores a la fecha faltante..
#
missing_days = df_long.groupby('fecha')['precio'].apply(lambda x: x.isna().sum())
missing_days = missing_days[missing_days > 0]


# e deben rellenar utilizando el promedio de los 3 días previos y los 3 días posteriores a la fecha faltante..
df_long['precio'] = df_long.groupby('fecha')['precio'].transform(
    lambda x: x.fillna(x.rolling(window=3, min_periods=1, center=True).mean())
)
#########3


##  4 Cálculos de Promedios
#
daily_avg = df_long.groupby('fecha')['precio'].mean().reset_index()
print("el promedio diario de precios",daily_avg)
daily_avg['precio_7d'] = daily_avg['precio'].rolling(window=7, min_periods=1).mean()
print()
print("promedio móvil de 7 días de los precios diarios.")
print()
print(daily_avg['precio_7d'])


# #6 Almacenamiento de Resultados

# for _, row in daily_avg.iterrows():
#     registro = PrecioEnergia(
#         fecha=row['fecha'],
#         precio_promedio=row['precio'],
#         precio_7d=row['precio_7d']
#     )
#     session.add(registro)


# session.commit()
# session.close()


plt.figure(figsize=(12, 6))
plt.plot(daily_avg['fecha'], daily_avg['precio'], label='Daily Average', marker='o')
plt.plot(daily_avg['fecha'], daily_avg['precio_7d'], label='7-Day Moving Average', linestyle='dashed')
plt.xlabel('Fecha')
plt.ylabel('Precio DE ENERGIA')
plt.title('Precio DE ENERGIA sobre el tiempo')
plt.legend()
plt.xticks(rotation=45)
plt.grid()
plt.savefig('image.png')
plt.show()

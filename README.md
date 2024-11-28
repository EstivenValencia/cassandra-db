# Validación de Tecnología de Zapatillas para mejorar la eficiencia de la UEFA Women's Champions League

## Caso de Uso

La empresa **Deusto Sport** ha creado una nueva tecnología de zapatillas de tenis que permite un mayor agarre en los campos de fútbol, independientemente de las condiciones meteorológicas. Según los resultados preliminares, la empresa asegura que el uso de estas zapatillas aumenta el rendimiento de los jugadores en un 10%. Para validar esta tecnología, la empresa ha decidido realizar un estudio basado en los partidos de la UEFA Women’s Champions League 2024/2025.

Para llevar a cabo el estudio, se recolectarán los datos generados durante todos los partidos. En cada juego, un equipo usará las nuevas zapatillas durante el primer tiempo, mientras que el equipo rival no las utilizará. En el segundo tiempo, los roles se invertirán. Además, cada jugadora llevará un sensor de signos vitales para medir la frecuencia cardiaca, el umbral aeróbico, el umbral anaeróbico, el gasto de oxígeno y la potencia. Estas mediciones se tomarán a una frecuencia de muestreo de 4 Hz durante todo el partido. El muestreo se realiza a esta frecuencia para capturar el comportamiento completo de la variable crítica de la frecuencia cardiaca.

Por cada partido, también se medirán las siguientes variables meteorológicas por minuto:

- Temperatura exterior
- Temperatura del campo
- Presión atmosférica
- Humedad relativa en el ambiente
- Humedad del campo
- Velocidad y dirección del viento
- Precipitación
- Calidad del aire


## 1. Ventajas y Desventajas de la Base de Datos NoSQL Seleccionada

Al analizar el caso de uso, se observa que el principal reto es la alta velocidad de escritura de datos, especialmente en lo que respecta al sensado de los datos vitales de las jugadoras. Se espera una tasa de 50 mediciones por segundo por cada variable y para cada jugadora. Además, en la primera ronda de la UEFA Women’s Champions League, se jugarán hasta 8 partidos simultáneamente, lo que genera el siguiente volumen de escrituras por segundo:

```python
partidos simultaneos x equipos x jugadoras x variables x tasa_muestreo = escrituras por segundo
8 x 2 x 11 x 4 x 4 = 2816 escrituras por segundo
```

Dado que cada partido tiene una duración de 90 minutos, el total de escrituras podría alcanzar los 15.206.400 registros durante los 8 partidos. A esto se deben añadir los datos meteorológicos, que aunque se toman con una frecuencia de un minuto, también contribuyen al volumen de escrituras. Este escenario plantea un reto en cuanto a la gestión eficiente de las inserciones de datos, especialmente cuando se gestionan picos de carga debido a la simultaneidad de los partidos.

Tras evaluar el problema, se ha optado por utilizar **Cassandra**, por las siguientes razones:

- **Escalabilidad y rendimiento**: Su capacidad para escalar horizontalmente es una ventaja, ya que se espera que el estudio se expanda a otros deportes en el futuro, como baloncesto, voleibol, senderismo, entre otros.

- **Alta disponibilidad**: Dado que los datos deben ser escritos en tiempo real y el estudio tiene un costo significativo, la base de datos debe estar disponible en todo momento para que los datos puedan ser insertados sin interrupciones.

- **Modelo de datos adecuado**: Aunque se manejarán grandes volúmenes de datos, la estructura de los datos es relativamente uniforme. Aunque algunos cambios en la estructura del esquema podrían ocurrir durante el estudio, no se espera que sean frecuentes, sino aislados.

- **Teorema de CAP**: En este caso, no es necesario garantizar la coherencia inmediata de los datos, ya que la lectura y análisis se realizarán una vez finalizados los partidos. Esto permite priorizar la disponibilidad y la partición de datos, sin que la falta de coherencia inmediata sea un inconveniente.

- **Experiencia del equipo con CQL**: El equipo de datos tiene una amplia experiencia con SQL, lo que permite aprovechar el lenguaje CQL de Cassandra, lo cual facilita la adaptación del equipo al nuevo sistema.

### Instalación de Cassandra 

Para la instalación se utilizo un docker de Cassandra y se ejecuto en local de la siguiente manera:

```bash
docker pull cassandra

docker run --name cassandra-big_data -p 9042:9042 -v cassandra-data:/var/lib/cassandra -e CASSANDRA_USER=admin -e CASSANDRA_PASSWORD=admin --hostname cassandra -d cassandra:latest
```

## 2. Esquema de la Base de Datos

El esquema de la base de datos está compuesto por las siguientes tablas:

1. **Tabla de Jugadoras**: Almacena la información general de las jugadoras.
2. **Tabla de Datos Fisiológicos de Jugadoras**: Almacena las mediciones fisiológicas (frecuencia cardíaca, umbral aeróbico, etc.) durante el partido.
3. **Tabla de Información del Campo de Fútbol**: Contiene detalles sobre el campo donde se juega el partido.
4. **Tabla de Datos Meteorológicos**: Almacena las mediciones meteorológicas durante el partido.
5. **Tabla de partidos**: Contiene la información de los equipos que compiten, los resultados de los marcadores, la relacion con la cancha id y las fechas de inicio y terminacion del juego.

### Creación del esquema

Para la creación del esquema se provee el script create_tables.py de python que utiliza la clase Cassandra definida en DB_cassandra_tools.py para comunicarse con la base de datos que se encuentra ejecutando en el docker, a su vez la clase se encarga de crear el espacio de trabajo sino existe y lo configura para utilizarlo en las siguientes consultas. El script se ejecuta como sigue acontinuación:

```bash
    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt

    python create_tables.py
```

El script define los siguientes esquemas para cada tabla

### Sentencia de creación de Tabla jugadoras

```cql

CREATE TABLE IF NOT EXISTS datos_generales_jugadoras (
    jugadora_id UUID,
    nombre TEXT,
    primer_apellido TEXT,
    segundo_apellido TEXT,
    posicion TEXT,
    edad INT,
    fecha_nacimiento DATE,
    ano_inicio_futbol INT,
    pais_nacimiento TEXT,
    pais_equipo TEXT,
    nombre_equipo TEXT,
    PRIMARY KEY (jugadora_id)
    );
```

Para esta tabla se crean indices segundarios para la utilizacion de filtros, correspondientes a los campos pais_equipo y ano_inicio_futbol. 

```cql
    CREATE INDEX ON datos_generales_jugadoras (pais_equipo);
    CREATE INDEX ON datos_generales_jugadoras (ano_inicio_futbol);
```

### Sentencia de creación de Tabla datos fisiologicos

```cql

    CREATE TABLE IF NOT EXISTS datos_fisiologicos (
        partido_id UUID,                
        jugadora_id UUID,               
        cancha_id UUID,
        timestamp TIMESTAMP,            
        frecuencia_cardiaca FLOAT,      
        umbral_aerobico FLOAT,          
        umbral_anaerobico FLOAT,        
        consumo_oxigeno FLOAT,          
        potencia FLOAT,                 
        PRIMARY KEY ((partido_id, jugadora_id, cancha_id), timestamp)
    );
```

### Sentencia de creación de Tabla con información del estadio

```cql

    CREATE TABLE IF NOT EXISTS informacion_cancha(
        cancha_id UUID,                
        ciudad TEXT,                
        longitud FLOAT,                
        ancho FLOAT,                  
        tipo_superficie TEXT,          
        altitud FLOAT,                 
        PRIMARY KEY (cancha_id));
```

### Sentencia de creación de Tabla datos meteorologicos

```cql

    CREATE TABLE IF NOT EXISTS datos_meteorologicos (
        partido_id UUID,
        cancha_id UUID,
        timestamp TIMESTAMP,
        temperatura_exterior FLOAT,
        temperatura_campo FLOAT,
        presion_atmosferica FLOAT,
        humedad_relativa FLOAT,
        humedad_campo FLOAT,
        velocidad_viento FLOAT,
        direccion_viento TEXT,
        precipitacion FLOAT,
        calidad_aire FLOAT,
        PRIMARY KEY (partido_id, cancha_id));
```

### Sentencia de creación de Tabla con datos de los partidos

```cql

    CREATE TABLE IF NOT EXISTS partidos (
        partido_id UUID,                     
        cancha_id UUID,
        fecha_inicio_juego TIMESTAMP,     
        fecha_terminacion_juego TIMESTAMP,                
        nombre_equipo_local text,            
        nombre_equipo_visitante text,        
        resultado_local INT,                 
        resultado_visitante INT,             
        PRIMARY KEY (partido_id, cancha_id));
```

Al finalizar la creacion de las tablas, se ejecuta la siguiente query para verificar la correcta creación de las tablas:

```python

    response = self.session.execute(f'DESCRIBE TABLE {table_name}')
    
    for row in response:
        print(row)
```

## 3. Sentencias de insercion

Para la inserción de los registros en la base de datos, se desarrolló el script synthetic_db.py. Este script utiliza listas predefinidas con valores específicos para cada variable, aplicando un muestreo aleatorio. Además, emplea la librería Faker para generar datos sintéticos de manera dinámica.

```bash

    python synthetic_db.py

```

El script se estructura en un conjunto de ciclos anidados. En primer lugar, se crean tres registros de estadios. Por cada estadio, se generan 200 registros con datos generales de jugadoras. Posteriormente, para cada jugadora, se crean tres partidos. En cada partido, se insertan tres registros de datos meteorológicos, y por cada registro meteorológico, se añaden 10 registros de datos fisiológicos.


### Registros de estadio

```python
    cancha_id = uuid4()
    ciudad = fake.city()
    longitud = random.uniform(-180, 180)
    ancho = random.uniform(30, 150)
    tipo_superficie = random.choice(["Cesped", "Tierra", "Sintética"])
    altitud = random.uniform(0, 5000)

    query = f"""
        INSERT INTO informacion_cancha (
            cancha_id, ciudad, longitud, ancho, tipo_superficie, altitud
        )
        VALUES (%s, %s, %s, %s, %s, %s);
    """
```

### Registros de jugadoras

```python

    jugadora_id = uuid4()
    nombre = fake.first_name_female()
    primer_apellido = fake.last_name()
    segundo_apellido = fake.last_name()
    posicion = random.choice(posiciones)
    edad = random.randint(17,60)
    fecha_nacimiento = fake.date_between(start_date='-40y', end_date='today')
    ano_inicio_futbol = random.randint(2000,2022)
    pais_nacimiento = fake.country()
    pais_equipo = random.choice(paises_equipo)
    nombre_equipo = random.choice(equipos_femeninos)

    query = f"""
        INSERT INTO datos_generales_jugadoras (
            jugadora_id, nombre, primer_apellido, segundo_apellido, posicion, edad,
            fecha_nacimiento, ano_inicio_futbol, pais_nacimiento, pais_equipo, nombre_equipo
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
```


### Registros de partidos

```python

    partido_id = uuid4()
    cancha_id = cancha_id
    fecha_inicio_juego = fake.date_time_this_year(before_now=True, after_now=False)
    fecha_terminacion_juego = fecha_inicio_juego + timedelta(hours=1)
    nombre_equipo_local = random.choice(equipos_femeninos)
    nombre_equipo_visitante = random.choice(equipos_femeninos)
    resultado_local = random.randint(0, 15)
    resultado_visitante = random.randint(0, 15)

    query = f"""
        INSERT INTO partidos (
            partido_id, cancha_id, fecha_inicio_juego, fecha_terminacion_juego, nombre_equipo_local, 
            nombre_equipo_visitante, resultado_local, resultado_visitante
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """

```


### Registros de datos meteorologicos

```python

    partido_id = partido_id
    cancha_id = cancha_id
    timestamp = datetime.datetime.now()
    temperatura_exterior = random.uniform(0, 40)
    temperatura_campo = random.uniform(20, 35)
    presion_atmosferica = random.uniform(950, 1050)
    humedad_relativa = random.uniform(20, 100)
    humedad_campo = random.uniform(10, 90)
    velocidad_viento = random.uniform(0, 20)
    direccion_viento = random.choice(direcciones_viento)
    precipitacion = random.uniform(0, 50)
    calidad_aire = random.uniform(0, 500)

    query = f"""
        INSERT INTO datos_meteorologicos (
            partido_id, cancha_id, timestamp, temperatura_exterior, temperatura_campo, 
            presion_atmosferica, humedad_relativa, humedad_campo, velocidad_viento, 
            direccion_viento, precipitacion, calidad_aire
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """


```


### Registros de datos fisioologicos

```python

    partido_id = partido_id
    jugadora_id = jugadora_id
    cancha_id = cancha_id
    timestamp = datetime.datetime.now()
    frecuencia_cardiaca = random.uniform(60, 200)
    umbral_aerobico = random.uniform(1.5, 2.5)
    umbral_anaerobico = random.uniform(2.5, 4.0)
    consumo_oxigeno = random.uniform(0.5, 3.5)
    potencia = random.uniform(100, 500)

    query = f"""
        INSERT INTO datos_fisiologicos (
            partido_id, jugadora_id, cancha_id, timestamp, frecuencia_cardiaca, 
            umbral_aerobico, umbral_anaerobico, consumo_oxigeno, potencia
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

```

En total se insertan las siguientes cantidades de registros por tabla:

| **Tabla**                     | **Cantidad de Registros** |
|-------------------------------|---------------------------|
| `datos_meteorologicos`         | 1800                     |
| `datos_fisiologicos`           | 52778                    |
| `datos_generales_jugadoras`    | 600                        |
| `partidos`                     | 1800                       |
| `informacion_cancha`           | 3                         |


## 4. Sentencias de modificacion para dos de los registros, cambiando el nombre de la jugadora a Mayúsculas.

Dado que al crear la tabla de información de las jugadoras se definió la clave primaria jugadora_id, es posible actualizar los datos de las jugadoras utilizando este atributo. Para realizar esta actualización, se utiliza el script update_instance.py:

```bash
    python update_instance.py
```

Este script ejecuta una consulta para obtener los dos primeros registros de la tabla datos_generales_jugadoras. Luego, actualiza los datos de estas jugadoras utilizando el método UPDATE, que convierte el nombre a mayúsculas. La actualización se filtra por la clave primaria jugadora_id. Finalmente, se ejecuta otra consulta para verificar que los cambios se hayan aplicado correctamente.

## 5. Consultas

Las siguientes consultas se pueden obtener ejecutando el archivo queries.py, pero antes es necesario realizar la configuración que se expone en el item a.2.

```bash 
    python queries.py
```

#### a.1 Consulta por una jugadora especifica filtrando por el año de comienzo en el football mayor de 2020

```cql 
    SELECT * FROM datos_generales_jugadoras WHERE ano_inicio_futbol > 2020 ALLOW FILTERING;
```

#### a.2 Consulta por una jugadora especifica filtrando que el equipo empiece “Manchester…..”

Por defecto, Cassandra no permite utilizar filtros LIKE a menos que se active un índice SASI, el cual es un comando experimental. Para habilitarlo, es necesario modificar las configuraciones del archivo YAML de Cassandra. Los pasos a seguir son los siguientes:

```bash
    docker exec -it cassandra-big_data bash
```

Dentro del contenedor debemos actualizar los paquetes e instalar vim

```bash
    apt-get update
    apt-get install vim
    vim /etc/cassandra/cassandra.yaml

```

Ya dentro de este archivo debemos buscar la seccion de SASI y poner sasi_indexes_enabled a true. luego cerramos el archivo y reiniciamos el contenedor. 

Dentro del script queries.py se crea el indice segundario SASI para nombre_equipo como se presenta a continuación:

```cql
    CREATE INDEX ON datos_generales_jugadoras (nombre_equipo)
    USING 'org.apache.cassandra.index.sasi.SASIIndex' 
    WITH OPTIONS = {'analyzer_class': 'org.apache.cassandra.index.sasi.analyzer.StandardAnalyzer', 
    'case_sensitive': 'false'};
```

La consulta para obtener las jugadoras que se encuentren en el equipo se muestra a continuación:

```cql
    SELECT * FROM datos_generales_jugadoras WHERE nombre_equipo LIKE 'Manchester%';
```

#### b. Consulta por un país concreto donde juega una jugadora

```cql
    SELECT * FROM datos_generales_jugadoras WHERE pais_equipo='Alemania';
```

### Tabla de tiempos

| **Consulta**                     | **Tiempo** |
|-------------------------------|---------------------------|
| `a1`         | 0.006833 seg                       |
| `a2`           | 0.020474 seg                   |
| `b`    | 0.009306 seg                       |

## 6. Conclusiones

En el caso de los tiempos de consulta, se observa una respuesta rápida gracias a la definición de los índices secundarios. Sin embargo, según la documentación de Cassandra, estos índices pueden ser menos eficientes que los filtros basados en claves primarias. Aun así, los índices secundarios son útiles para realizar filtros ocasionales sobre columnas que no fueron consideradas durante el diseño inicial del esquema.

Por otro lado, se evidencia la ineficiencia del uso del comando LIKE, que aún se encuentra en una fase temprana de desarrollo en Cassandra. Para emplearlo, es necesario definir un índice SASI en la columna que se desea filtrar. Durante las pruebas, se comprobó que las consultas con LIKE son hasta tres veces más lentas que las consultas normales. Además, esta diferencia podría aumentar de forma no lineal a medida que crece el volumen de datos en la base de datos.

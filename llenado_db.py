import random
from faker import Faker
from uuid import uuid4
from DB_cassandra_tools import Cassandra
import datetime
from datetime import timedelta

if __name__ == '__main__':
    fake = Faker()

    ip = '127.0.0.1'
    port = 9042
    keyspace = 'futbol'

    cassandra = Cassandra(ip, port)
    cassandra.create_keyspace(keyspace)

    
    posiciones = [
        "Delantera","Centrocampista",
        "Defensora","Portera",
        "Extremo","Mediocampista ofensiva",
        "Mediocampista defensiva","Lateral derecho",
        "Lateral izquierdo","Central"
    ]

    paises_equipo = [
        "Alemania","Francia",
        "Suecia","Inglaterra",
        "España","Países Bajos",
        "Italia","Noruega",
        "Dinamarca","Finlandia",
        "Rusia","Suiza",
        "Portugal","Bélgica",
        "Escocia","Austria",
        "República Checa","Polonia",
        "Irlanda","Islandia"
    ]

    equipos_femeninos = [
        "Manchester United Women","Manchester City Women",
        "Chelsea FC Women","Arsenal Women",
        "FC Barcelona Femení","Olympique Lyonnais Féminin",
        "Paris Saint-Germain Féminine","Bayern Munich Frauen",
        "VfL Wolfsburg Frauen","Juventus Women",
        "Real Madrid Femenino","Atletico Madrid Femenino",
        "AS Roma Women","AC Milan Women",
        "Ajax Vrouwen","Rosengård",
        "BK Häcken","SL Benfica Women",
        "Sporting CP Women","Glasgow City FC"
    ]

    direcciones_viento = ["Norte", "Sur", "Este", "Oeste", "Noreste", "Suroeste", "Sureste", "Noroeste"]

    # Se simula la informacion de tres canchas de futbol
    for _ in range(3):
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

        data = (cancha_id, ciudad, longitud, ancho, tipo_superficie, altitud)

        cassandra.execute_command(query, data)

        # Por cada cancha se simulan 20 datos de jugadoras
        for _ in range(20):
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

            data = (jugadora_id, nombre, primer_apellido, segundo_apellido, posicion, edad,
                    fecha_nacimiento, ano_inicio_futbol, pais_nacimiento, pais_equipo, nombre_equipo)

            cassandra.execute_command(query, data)

            # Para cada jugadora se simulan 3 partidos
            for _ in range(3):
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

                data = (partido_id, cancha_id, fecha_inicio_juego, fecha_terminacion_juego, 
                        nombre_equipo_local, nombre_equipo_visitante, resultado_local, resultado_visitante)

                cassandra.execute_command(query, data)

                # Por cada partido se simulan 10 datos meteorologicos, debido a que se planteo que esta medida se
                # tomaría por minuto
                for _ in range(10):
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

                    data = (partido_id, cancha_id, timestamp, temperatura_exterior, temperatura_campo, 
                            presion_atmosferica, humedad_relativa, humedad_campo, velocidad_viento, 
                            direccion_viento, precipitacion, calidad_aire)

                    cassandra.execute_command(query, data)

                    # Por cada medicion meteorologica se simulan 50 datos fisiologicos por cada jugadora
                    for _ in range(50):
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

                        data = (partido_id, jugadora_id, cancha_id, timestamp, frecuencia_cardiaca, 
                                umbral_aerobico, umbral_anaerobico, consumo_oxigeno, potencia)

                        cassandra.execute_command(query, data)

        
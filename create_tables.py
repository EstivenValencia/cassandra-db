from DB_cassandra_tools import Cassandra

if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 9042
    keyspace = 'futbol'

    cassandra = Cassandra(ip, port)
    cassandra.create_keyspace(keyspace)

    table_players = """
    CREATE TABLE IF NOT EXISTS datos_generales_jugadoras (

        jugadora_id UUID,               
        nombre text,
        primer_apellido text, 
        segundo_apellido text,
        posicion text,
        edad int,
        fecha_nacimiento date,
        ano_inicio_futbol int,
        pais_nacimiento text,
        pais_equipo text,
        nombre_equipo text,
        PRIMARY KEY (jugadora_id));
    """

    table_player_physiology = """
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
    """

    table_playing_field = """
    CREATE TABLE IF NOT EXISTS informacion_cancha(
        cancha_id UUID,                
        ciudad TEXT,                
        longitud FLOAT,                
        ancho FLOAT,                  
        tipo_superficie TEXT,          
        altitud FLOAT,                 
        PRIMARY KEY (cancha_id));
    """

    table_meteorology = """
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
    """

    table_soccer_game = """
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
    """

    # Creacion de la tabla de jugadoras
    cassandra.create_column_family(table_players,"datos_generales_jugadoras")

    # Creacion de indices segundarios para la tabla datos generales jugadores
    query = """
                CREATE INDEX ON datos_generales_jugadoras (pais_equipo);
            """
    cassandra.execute_command(query)

    query = """
                CREATE INDEX ON datos_generales_jugadoras (ano_inicio_futbol);
            """
    cassandra.execute_command(query)

    # Creacion de la tabla para los datos fisiologicos de las jugadoras por partido
    cassandra.create_column_family(table_player_physiology,"datos_fisiologicos")

    # Creacion de la tabla con los datos del estadio
    cassandra.create_column_family(table_playing_field, "informacion_cancha")

    # Creacion de la tabla con los datos meteorologicos del estadio 
    cassandra.create_column_family(table_meteorology,"datos_meteorologicos")

    # Creacion de la tabla con los datos sobre el partido jugado
    cassandra.create_column_family(table_soccer_game,"partidos")
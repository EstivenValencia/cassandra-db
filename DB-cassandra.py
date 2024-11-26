from cassandra.cluster import Cluster


class Cassandra:
    def __init__(self, ip, port) -> None:
        self.ip = ip
        self.port = port

    def create_keyspace(self, keyspace) -> bool:
        try:
            # Conexion al cluster de cassandra utilizando la ip local que esta mapeada sobre la red del docker
            # sobre el puerto
            self.cluster =  Cluster(contact_points=[self.ip], port=self.port) 
            self.session = self.cluster.connect()

            # Creamos del espacio de trabajo denominado futbol en caso de no existir
            self.session.execute(f"""
                CREATE KEYSPACE IF NOT EXISTS {keyspace} WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}}
            """)

            # Usamos el espacio de trabajo creado anteriormente
            self.session.set_keyspace(keyspace)
            print("creacion de espacio de trabajo")

            return True
        
        except Exception as err:
            print(f"No fue posible la conexion [{err}]")
            return False
        
    def create_table(self, schema) -> None:
        try:
            self.session.execute(schema)

            # rows = self.session.execute("SELECT * FROM datos_generales_jugadoras")
            # for row in rows:        
            #     print(row.jugadora_id)
            return True
        except Exception as err:
            print(f"ERROR [{err}]")
            return False
        

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
        pais_juego text,
        nombre_equipo text,
        PRIMARY KEY (jugadora_id, nombre_equipo));
    """

    table_player_physiology = """
    CREATE TABLE IF NOT EXISTS datos_fisiologicos (
        partido_id UUID,                -- Identificador del partido
        jugadora_id UUID,               -- Identificador único de la jugadora
        cancha_id UUID,
        timestamp TIMESTAMP,            -- Tiempo exacto de la medición
        frecuencia_cardiaca FLOAT,      -- Frecuencia cardiaca en latidos por minuto (lpm)
        umbral_aerobico FLOAT,          -- Umbral aeróbico en bpm
        umbral_anaerobico FLOAT,        -- Umbral anaeróbico en bpm
        consumo_oxigeno FLOAT,          -- Consumo de oxígeno en ml/kg/min
        potencia FLOAT,                 -- Potencia en vatios (W)
        PRIMARY KEY ((partido_id, jugadora_id, cancha_id), timestamp)
    );
    """

    table_playing_field = """
    CREATE TABLE IF NOT EXISTS informacion_cancha(
        cancha_id UUID,                -- Identificador único de la cancha
        ubicacion TEXT,                -- Ubicación de la cancha (ciudad, país, etc.)
        longitud FLOAT,                -- Longitud de la cancha en metros (ej. 105 metros)
        ancho FLOAT,                   -- Ancho de la cancha en metros (ej. 68 metros)
        tipo_superficie TEXT,          -- Tipo de superficie (ej. "césped natural", "césped sintético", "tierra", etc.)
        altitud FLOAT,                 -- Altitud sobre el nivel del mar en metros (ej. 300 metros)
        PRIMARY KEY (cancha_id));
    """

    table_meteorology = """
    CREATE TABLE IF NOT EXISTS datos_generales_jugadoras (
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
    CREATE TABLE IF NOT EXISTS partido (
        partido_id UUID,                     -- Identificador único del partido
        cancha_id UUID,
        fecha TIMESTAMP,                      -- Fecha y hora del partido
        nombre_equipo_local text,                 -- Referencia al equipo local
        nombre_equipo_visitante text,             -- Referencia al equipo visitante
        resultado_local INT,                  -- Goles del equipo local
        resultado_visitante INT,              -- Goles del equipo visitante
        PRIMARY KEY (partido_id, cancha_id));
    """

    cassandra.create_table(table_players)
    cassandra.create_table(table_player_physiology)
    cassandra.create_table(table_playing_field)
    cassandra.create_table(table_meteorology)
    cassandra.create_table(table_soccer_game)
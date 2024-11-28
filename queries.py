from DB_cassandra_tools import Cassandra

if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 9042
    keyspace = 'futbol'

    cassandra = Cassandra(ip, port)
    cassandra.create_keyspace(keyspace)

    ####################################
    #           consulta a.1
    ####################################

    # Consulta de jugadora filtrando por el ano de comienzo en el futbol mayor a 2020
    query = """
            SELECT * FROM datos_generales_jugadoras WHERE ano_inicio_futbol > 2020 ALLOW FILTERING;
        """

    # El parametro trace permite obtener los metadatos de la ejecucion
    response = cassandra.execute_command(query, trace=True)

    print("Contenido de la respuesta de la consulta a.1\n\n\n")
    for row in response:
        print(row)


    # Se obtiene el tiempo de los metadatos de la consulta
    duration_seconds_a1 = response.get_query_trace().duration.total_seconds()

    ####################################
    #           consulta a.2
    ####################################

    # Se crea un indice SASI en cassandra para la columna nombre equipo lo que permite el uso de LIKE
    query = """
            CREATE INDEX ON datos_generales_jugadoras (nombre_equipo)
            USING 'org.apache.cassandra.index.sasi.SASIIndex' 
            WITH OPTIONS = {'analyzer_class': 'org.apache.cassandra.index.sasi.analyzer.StandardAnalyzer', 
            'case_sensitive': 'false'};
        """

    cassandra.execute_command(query)

    # Consulta de jugadora filtrando por una jugadora especifica filtrando que el equipo empiece "Manchester..."
    query = """
            SELECT * FROM datos_generales_jugadoras WHERE nombre_equipo LIKE 'Manchester%';
        """

    # El parametro trace permite obtener los metadatos de la ejecucion
    response = cassandra.execute_command(query, trace=True)

    print("Contenido de la respuesta de la consulta a.2\n\n\n")
    for row in response:
        print(row)

    # Se obtiene el tiempo de los metadatos de la consulta
    duration_seconds_a2 = response.get_query_trace().duration.total_seconds()
    

    ####################################
    #           consulta b
    ####################################

    # Consulta de jugadora por un pais concreto en el que juega
    query = """
            SELECT * FROM datos_generales_jugadoras WHERE pais_equipo='Alemania';
        """

    # El parametro trace permite obtener los metadatos de la ejecucion
    response = cassandra.execute_command(query, trace=True)

    print("Contenido de la respuesta de la consulta b\n\n\n")
    for row in response:
        print(row)

    # Se obtiene el tiempo de los metadatos de la consulta
    duration_seconds_b = response.get_query_trace().duration.total_seconds()

    # TIEMPOS
    print(f"\n\n\nEl tiempo que demora la consulta a.1 es: {duration_seconds_a1} seg")
    print(f"El tiempo que demora la consulta a.2 es: {duration_seconds_a2} seg")
    print(f"El tiempo que demora la consulta b es: {duration_seconds_b} seg")
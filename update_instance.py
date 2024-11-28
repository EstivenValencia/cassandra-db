from DB_cassandra_tools import Cassandra

if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 9042
    keyspace = 'futbol'

    cassandra = Cassandra(ip, port)
    cassandra.create_keyspace(keyspace)

    # Se leen los dos primeros campos de la tabla de jugadoras
    query = 'SELECT * FROM datos_generales_jugadoras LIMIT 2'

    response = cassandra.execute_command(query)

    for row in response:
        # Se actualizan los nombres de dos de las jugadoras y se ponen en mayusculas
        query = f"UPDATE datos_generales_jugadoras SET nombre='{row.nombre.upper()}' WHERE jugadora_id={row.jugadora_id};"
        cassandra.execute_command(query)

    # Verificacion de la actualizacion
    query = 'SELECT * FROM datos_generales_jugadoras LIMIT 2'
    response = cassandra.execute_command(query)

    for row in response:
        print(row.nombre)


    

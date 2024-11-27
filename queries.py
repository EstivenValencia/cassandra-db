from DB_cassandra_tools import Cassandra

if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 9042
    keyspace = 'futbol'

    cassandra = Cassandra(ip, port)
    cassandra.create_keyspace(keyspace)

    

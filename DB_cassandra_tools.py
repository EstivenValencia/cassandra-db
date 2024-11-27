from cassandra.cluster import Cluster
import random


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
        
    def create_column_family(self, schema, table_name) -> None:
        try:
            self.session.execute(schema)

            response = self.session.execute(f'DESCRIBE TABLE {table_name}')
            
            for row in response:
                print(row)
            
            return True
        except Exception as err:
            print(f"ERROR [{err}]")
            return False
        
    def execute_command(self, query, data=None) -> None:
        try:
            if data is None:
                self.session.execute(query)
            else:
                self.session.execute(query, data)

        except Exception as err:
            print(f"ERROR [{err}]")
        
        return None

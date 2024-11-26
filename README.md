# Proyecto: Validación de Tecnología de Zapatillas Deusto Sport en la UEFA Women's Champions League 2024/2025

## Caso de Uso

### PRELIMINAR

La empresa Deusto Sport ha creado una nueva tecnología de zapatillas de tenis que permite un mayor agarre en los campos de fútbol independientemente de las circunstancias meteorológicas. Según los resultados preliminares, asegura un incremento en el rendimiento de los jugadores de un 10%. Para validar esta nueva tecnología, la empresa decide realizar un estudio en el que evaluará el rendimiento de todos los equipos de la UEFA Women's Champions League de la temporada 2024/2025 ([enlace al calendario](https://www.relevo.com/futbol/champions-league-femenina/empieza-champions-league-femenina-20242025-20240902141346-nt.html)).

En este estudio, se recogerán los datos generados durante todos los partidos. En cada partido, las jugadoras de un equipo usarán las nuevas zapatillas durante el primer tiempo, mientras que el equipo rival no lo hará. En el segundo tiempo, los roles se invertirán: el equipo que no usó las zapatillas las llevará, y viceversa.

Además, cada jugadora llevará un sensor de signos vitales que medirá la frecuencia cardíaca, umbral aeróbico, umbral anaeróbico, gasto de oxígeno y potencia a una frecuencia de muestreo de 50 Hz. Por cada partido, también se medirán variables meteorológicas como temperatura, presión, humedad, viento, precipitación y calidad del aire, con una muestra por minuto a través de equipos de monitoreo con un error de medición de 0.001%.

### MEJORADO

La empresa Deusto Sport, especializada en innovación deportiva, ha desarrollado una nueva tecnología aplicada a zapatillas de tenis que promete revolucionar el rendimiento en campos de fútbol bajo cualquier condición meteorológica. Estas zapatillas ofrecen un agarre superior y, según estudios preliminares, incrementan el rendimiento de los jugadores en un 10%.

#### Diseño del Estudio
**Metodología de evaluación**:
- Durante cada partido, un equipo usará las zapatillas Deusto Sport durante el primer tiempo, mientras que el equipo rival no las usará. En el segundo tiempo, los roles se invertirán.

**Datos recolectados por jugadora**:
Cada jugadora estará equipada con un sensor de monitoreo fisiológico que registrará las siguientes métricas:
- Frecuencia cardíaca.
- Umbral aeróbico.
- Umbral anaeróbico.
- Consumo de oxígeno.
- Potencia.
  
Estas mediciones se realizarán a una frecuencia de 4 Hz, para captar el comportamiento completo de la frecuencia cardíaca.

**Datos meteorológicos**:
Durante cada partido, se registrarán variables climáticas clave como:
- Temperatura exterior.
- Temperatura del campo.
- Presión atmosférica.
- Humedad relativa en el ambiente.
- Humedad del campo de fútbol.
- Velocidad y dirección del viento.
- Precipitación.
- Calidad del aire.

Estas mediciones se tomarán a intervalos de un minuto, con un error de medida de 0.001%.

---

## Ventajas y Desventajas de la BD NoSQL seleccionada

**Ventajas de Cassandra**:
- **Velocidad de escritura**: Cassandra está diseñada para manejar grandes volúmenes de datos de escritura, lo cual es crucial en este estudio debido a la alta tasa de muestreo y la cantidad de partidos simultáneos.
- **Escalabilidad**: Cassandra es altamente escalable, lo que permitirá manejar el crecimiento del estudio y la inclusión de otros deportes como baloncesto, voleibol, entre otros.
- **Disponibilidad**: Garantiza una alta disponibilidad, lo que es esencial dado que los datos deben escribirse continuamente durante los partidos, incluso en situaciones de picos de tráfico.
- **Resiliencia**: Cassandra ofrece tolerancia a fallos y redundancia, asegurando que la base de datos esté disponible incluso en caso de fallos en algunos nodos.

**Desventajas de Cassandra**:
- **Complejidad en las consultas**: Realizar consultas complejas que involucren `JOIN` o relaciones entre varias tablas puede ser más difícil y menos eficiente en Cassandra, lo cual es un reto cuando se desea analizar el impacto de las condiciones meteorológicas en el rendimiento de las jugadoras.
- **Consistencia**: Cassandra usa un modelo de consistencia eventual, lo que significa que no garantiza una consistencia inmediata en todas las réplicas. Sin embargo, dado que las lecturas y análisis se realizarán después de los partidos, esta desventaja es aceptable.

---

## Esquema y Sentencias de Creación

### Tablas

1. **Tabla Jugadora**:
```sql
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
    pais_juego TEXT,
    nombre_equipo TEXT,
    PRIMARY KEY (jugadora_id, nombre_equipo));
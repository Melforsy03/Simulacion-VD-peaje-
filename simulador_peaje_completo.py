
import random
import heapq
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Clase de evento para la simulación
class Evento:
    def __init__(self, tiempo, tipo, cabina_id=None):
        self.tiempo = tiempo
        self.tipo = tipo
        self.cabina_id = cabina_id

    def __lt__(self, otro):
        return self.tiempo < otro.tiempo

# Función principal de simulación
def simular_peaje(tasa_llegada, tasa_servicio, tiempo_total, num_cabinas):
    reloj = 0
    eventos = []
    heapq.heappush(eventos, Evento(random.expovariate(tasa_llegada), 'llegada'))
    cabinas = [None] * num_cabinas
    cola = []
    tiempos_espera = []
    ocupacion_cabinas = [0] * num_cabinas
    tiempo_anterior = 0

    while eventos:
        evento = heapq.heappop(eventos)
        reloj = evento.tiempo
        if reloj > tiempo_total:
            break
        for i in range(num_cabinas):
            if cabinas[i] is not None:
                ocupacion_cabinas[i] += (reloj - tiempo_anterior)
        tiempo_anterior = reloj

        if evento.tipo == 'llegada':
            cabina_libre = next((i for i, cabina in enumerate(cabinas) if cabina is None), None)
            if cabina_libre is not None:
                duracion = random.expovariate(tasa_servicio)
                salida = reloj + duracion
                cabinas[cabina_libre] = salida
                heapq.heappush(eventos, Evento(salida, 'salida', cabina_libre))
                tiempos_espera.append(0)
            else:
                cola.append(reloj)
            proxima_llegada = reloj + random.expovariate(tasa_llegada)
            heapq.heappush(eventos, Evento(proxima_llegada, 'llegada'))
        elif evento.tipo == 'salida':
            cabinas[evento.cabina_id] = None
            if cola:
                llegada_cliente = cola.pop(0)
                espera = reloj - llegada_cliente
                tiempos_espera.append(espera)
                duracion = random.expovariate(tasa_servicio)
                salida = reloj + duracion
                cabinas[evento.cabina_id] = salida
                heapq.heappush(eventos, Evento(salida, 'salida', evento.cabina_id))

    promedio_espera = sum(tiempos_espera) / len(tiempos_espera) if tiempos_espera else 0
    return promedio_espera, len(tiempos_espera), ocupacion_cabinas

# Parámetros y ejecución
cabinas_list = [2, 3, 4]
tiempos_totales = [300, 500]
tasas_llegada = [1/4, 1/5]
tasas_servicio = [1/3, 1/4]
num_simulaciones = 10
resultados = []

for cabinas in cabinas_list:
    for tiempo_total in tiempos_totales:
        for tasa_llegada in tasas_llegada:
            for tasa_servicio in tasas_servicio:
                for _ in range(num_simulaciones):
                    espera, atendidos, ocupacion = simular_peaje(tasa_llegada, tasa_servicio, tiempo_total, cabinas)
                    resultados.append({
                        "Cabinas": cabinas,
                        "Tiempo Total": tiempo_total,
                        "Tasa Llegada": round(tasa_llegada, 3),
                        "Tasa Servicio": round(tasa_servicio, 3),
                        "Tiempo promedio espera": espera,
                        "Autos atendidos": atendidos,
                        "Ocupación promedio (%)": np.mean([100 * o / tiempo_total for o in ocupacion])
                    })

df_resultados = pd.DataFrame(resultados)
df_resultados.to_csv("resultados_simulacion.csv", index=False)

# Gráficos
sns.set(style="whitegrid")
plt.figure(figsize=(8, 5))
sns.histplot(df_resultados["Tiempo promedio espera"], kde=True, bins=20)
plt.title("Distribución del Tiempo Promedio de Espera")
plt.xlabel("Tiempo promedio de espera (s)")
plt.ylabel("Frecuencia")
plt.tight_layout()
plt.savefig("hist_espera.png")
plt.close()

plt.figure(figsize=(8, 5))
sns.boxplot(x="Cabinas", y="Ocupación promedio (%)", data=df_resultados)
plt.title("Boxplot de Ocupación Promedio por Número de Cabinas")
plt.xlabel("Número de cabinas")
plt.ylabel("Ocupación promedio (%)")
plt.tight_layout()
plt.savefig("box_ocupacion.png")
plt.close()

plt.figure(figsize=(8, 5))
sns.lineplot(data=df_resultados, x="Cabinas", y="Tiempo promedio espera", ci="sd", estimator="mean", marker="o")
plt.title("Tiempo promedio de espera según número de cabinas")
plt.xlabel("Número de cabinas")
plt.ylabel("Tiempo promedio de espera (s)")
plt.tight_layout()
plt.savefig("line_espera.png")
plt.close()

plt.figure(figsize=(8, 5))
sns.scatterplot(data=df_resultados, x="Ocupación promedio (%)", y="Tiempo promedio espera", hue="Cabinas", palette="tab10")
plt.title("Dispersión entre ocupación y espera promedio")
plt.xlabel("Ocupación promedio (%)")
plt.ylabel("Tiempo promedio de espera (s)")
plt.tight_layout()
plt.savefig("scatter_ocupacion.png")
plt.close()

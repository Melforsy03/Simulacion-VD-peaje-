
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random


# funcion para generar tiempo de llegada
def generar_tiempoLL(lambd):
    return np.random.exponential(1 / lambd)

#funcion para generar tiempo de servicio 
def generar_tiempoServ(mu):
    return np.random.exponential(1 / mu)

def simular_peaje(num_servidores, lambd, mu, tiempo_total):
    reloj = 0
    tA = generar_tiempoLL(lambd)
    tS = [float('inf')] * num_servidores
    servidores = [None] * num_servidores
    cola = []
    NA = 0
    salida = {}
    llegada = {}

    C = [0] * num_servidores

    while reloj < tiempo_total:
        eventos = [tA] + tS
        prox_evento = min(eventos)
        reloj = prox_evento

        if tA == prox_evento:
            NA += 1
            llegada[NA] = reloj
            tA = reloj + generar_tiempoLL(lambd)

            libre = next((i for i, v in enumerate(servidores) if v is None), None)
            if libre is not None:
                servidores[libre] = NA
                tS[libre] = reloj + generar_tiempoServ(mu)
            else:
                cola.append(NA)
        else:
            idx_servidor = eventos.index(prox_evento) - 1
            cliente = servidores[idx_servidor]
            salida[cliente] = reloj
            C[idx_servidor] += 1

            if cola:
                nuevo = cola.pop(0)
                servidores[idx_servidor] = nuevo
                tS[idx_servidor] = reloj + generar_tiempoServ(mu)
            else:
                servidores[idx_servidor] = None
                tS[idx_servidor] = float('inf')

    tiempos_espera = [salida[i] - llegada[i] for i in llegada if i in salida]
    ocupacion = [c / NA * 100 for c in C]

    return {
        "espera_promedio": np.mean(tiempos_espera),
        "clientes_atendidos": len(salida),
        "ocupacion_promedio": np.mean(ocupacion)
    }

# simulaciones a probar 
resultados = []
simulaciones_por_config = 10
tiempos = [300, 500]
servidores = [2, 3, 4]
tasas_llegada = [0.2, 0.25]
tasas_servicio = [0.25, 0.33]

for tiempo_total in tiempos:
    for num_s in servidores:
        for lambd in tasas_llegada:
            for mu in tasas_servicio:
                for _ in range(simulaciones_por_config):
                    res = simular_peaje(num_s, lambd, mu, tiempo_total)
                    res.update({
                        "Cabinas": num_s,
                        "T Total": tiempo_total,
                        "Tasa Llegada": lambd,
                        "Tasa Servicio": mu
                    })
                    resultados.append(res)

df = pd.DataFrame(resultados)
df = df[["Cabinas", "T Total", "Tasa Llegada", "Tasa Servicio", "espera_promedio", "clientes_atendidos", "ocupacion_promedio"]]
df.columns = ["Cabinas", "T Total", "Tasa Llegada", "Tasa Servicio", "T promedio espera", "Autos atendidos", "Ocupación promedio (%)"]


csv_path = "./resultados.csv"
df.to_csv(csv_path, index=False)

# Gráfico
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="Cabinas", y="T promedio espera")
plt.title("Distribución del tiempo promedio de espera por cantidad de cabinas")
plt.tight_layout()
plt.savefig("./boxplot_espera_cabinas.png")


# Histograma del tiempo promedio de espera
plt.figure(figsize=(8, 5))
sns.histplot(df["T promedio espera"], bins=15, kde=True)
plt.title("Histograma del Tiempo Promedio de Espera")
plt.xlabel("Tiempo promedio de espera")
plt.ylabel("Frecuencia")
plt.tight_layout()
plt.savefig("histograma_espera.png")

# Boxplot de la ocupación promedio por cabinas
plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="Cabinas", y="Ocupación promedio (%)")
plt.title("Distribución de Ocupación Promedio por Cabinas")
plt.tight_layout()
plt.savefig("boxplot_ocupacion.png")

# Scatterplot: Tasa de llegada vs Tiempo promedio de espera
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="Tasa Llegada", y="T promedio espera", hue="Cabinas", palette="viridis")
plt.title("Tasa de Llegada vs Tiempo Promedio de Espera")
plt.tight_layout()
plt.savefig("scatter_llegada_espera.png")

# Lineplot: Cabinas vs tiempo promedio de espera promedio
mean_espera = df.groupby("Cabinas")["T promedio espera"].mean().reset_index()
plt.figure(figsize=(8, 5))
sns.lineplot(data=mean_espera, x="Cabinas", y="T promedio espera", marker="o")
plt.title("Tiempo Promedio de Espera Promediado por Número de Cabinas")
plt.tight_layout()
plt.savefig("line_espera_promedio.png")

# Scatterplot: Ocupación vs Tiempo de Espera
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="Ocupación promedio (%)", y="T promedio espera", hue="Cabinas", palette="coolwarm")
plt.title("Relación entre Ocupación y Tiempo de Espera")
plt.tight_layout()
plt.savefig("scatter_ocupacion_espera.png")

csv_path

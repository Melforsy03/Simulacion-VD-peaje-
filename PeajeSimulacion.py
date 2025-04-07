import random
import heapq

class Evento:
    def __init__(self, tiempo, tipo, cabina_id=None):
        self.tiempo = tiempo
        self.tipo = tipo  
        self.cabina_id = cabina_id

    def __lt__(self, otro):
        return self.tiempo < otro.tiempo

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

        # Actualizar ocupación de cabinas
        for i in range(num_cabinas):
            if cabinas[i] is not None:
                ocupacion_cabinas[i] += (reloj - tiempo_anterior)
        tiempo_anterior = reloj

        if evento.tipo == 'llegada':
            # Buscar cabina libre
            cabina_libre = None
            for i in range(num_cabinas):
                if cabinas[i] is None:
                    cabina_libre = i
                    break

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

if __name__ == "__main__":
    espera, atendidos, ocupacion = simular_peaje(
        tasa_llegada=1/5,
        tasa_servicio=1/4,
        tiempo_total= 500,
        num_cabinas= 4
    )

    print(f"Tiempo promedio de espera: {espera:.2f} segundos")
    print(f"Total de autos atendidos: {atendidos}")
    for i, tiempo in enumerate(ocupacion):
        porcentaje = 100 * tiempo / 25
        print(f"Cabina {i+1}: {porcentaje:.2f}% del tiempo ocupada")

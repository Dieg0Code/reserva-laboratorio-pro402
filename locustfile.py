import random

from locust import HttpUser, between, task


class PersonaQueReserva(HttpUser):
    wait_time = between(1, 3)

    @task(4)
    def mirar_bloques(self):
        self.client.get("/bloques")

    @task(1)
    def intentar_reservar(self):
        n = random.randint(1, 10_000_000)
        datos = {
            "nombre": "Persona de prueba",
            "rut": f"{n}-{n % 10}",
            "correo_electronico": f"persona{n}@ejemplo.cl",
            "bloque": random.randint(1, 8),
            "personas": random.randint(1, 30),
        }
        with self.client.post("/reservas", json=datos, catch_response=True) as respuesta:
            if respuesta.status_code in (201, 409):
                respuesta.success()

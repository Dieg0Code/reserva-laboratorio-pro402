# Reserva de laboratorio

Proyecto de demostración del módulo **PRO402 · Taller de Testing y Calidad de Software** (AIEP,
2026). Es un sistema pequeño para reservar bloques de un laboratorio: una API hecha con FastAPI, una
base de datos SQLite y una interfaz web, acompañadas de las pruebas que el módulo fue construyendo
sesión a sesión.

El sistema tiene **defectos conocidos a propósito**. Varias pruebas fallan porque describen algo
que el sistema todavía no hace bien, y esa es su función: mostrar qué se sabe y qué falta.

Todos los datos del proyecto son inventados. Ningún nombre, RUT ni correo pertenece a una persona
real.

## Qué hay en el repositorio

| Ruta | Contenido |
|---|---|
| `api.py`, `almacen.py`, `reservas.py`, `sala.py` | La aplicación: la API, el acceso a la base de datos y las reglas de negocio |
| `interfaz/` | La interfaz web |
| `test_*.py` | Las pruebas de Python, ejecutadas con `pytest` |
| `e2e/` | Las pruebas de extremo a extremo, ejecutadas con Playwright en un navegador real |
| `REQUISITOS.md` | Los requisitos del sistema, con su identificador |
| `trazabilidad.py` | Genera la matriz que cruza los requisitos con las pruebas que los comprueban |
| `locustfile.py` | La prueba de carga, ejecutada con Locust |
| `.github/workflows/` | El pipeline de integración continua |

## Requisitos para ejecutarlo

- [uv](https://docs.astral.sh/uv/), que instala Python y las dependencias del proyecto.
- [Node.js](https://nodejs.org/) 22 o superior, para las pruebas de extremo a extremo.

## Instalar y ejecutar

```bash
uv sync
uv run uvicorn api:app --reload
```

La interfaz queda disponible en <http://127.0.0.1:8000>.

## Ejecutar las pruebas

Las pruebas de Python:

```bash
uv run pytest -q
```

Las pruebas de extremo a extremo, desde la carpeta `e2e`. La primera vez hay que instalar las
dependencias y los navegadores:

```bash
cd e2e
npm ci
npx playwright install
npx playwright test
```

Playwright arranca el servidor por su cuenta antes de ejecutar las pruebas.

## Integración continua

Cada `push` y cada `pull request` ejecutan el flujo `.github/workflows/pruebas.yml` en los servidores
de GitHub Actions. Sus resultados se ven en la pestaña **Actions** del repositorio.

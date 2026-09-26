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

## Rojos conocidos

Estas pruebas fallan porque el sistema todavía no hace lo que ellas piden. No se borraron ni se
apagaron: están marcadas como **falla esperada**, con el motivo escrito en la propia prueba. La marca
es estricta: el día que el sistema se corrija y la prueba pase, el pipeline se pone en rojo para
obligar a quitar la marca.

| Prueba | Qué muestra | Qué decisión falta |
|---|---|---|
| `test_seguridad.py::test_otra_persona_no_puede_agotar_la_cuota_de_ana` | La API acepta cualquier RUT sin comprobar quién lo escribe, así que otra persona puede gastar la cuota de Ana | Cómo se identifican las personas |
| `e2e/pruebas/reserva.spec.ts` · «si falta un dato, la pantalla dice cuál corregir» | La pantalla muestra `[object Object]` en lugar de decir qué campo falta | Qué dice el mensaje de cada campo |
| `e2e/pruebas/verificacion.spec.ts` · «en una pantalla de 320 píxeles no hay desplazamiento horizontal» | La página mide más de 320 píxeles de ancho y obliga a desplazarse hacia los lados (WCAG 1.4.10) | Cómo se rediseña la grilla para pantallas angostas |

## Integración continua

Cada `push` y cada `pull request` ejecutan el flujo `.github/workflows/pruebas.yml` en los servidores
de GitHub Actions: los controles estáticos, las pruebas de Python y las de extremo a extremo. La
ejecución publica además la matriz de trazabilidad en su página de resumen.

El flujo `.github/workflows/auditoria.yml` revisa las dependencias de producción contra las bases
públicas de vulnerabilidades conocidas. Se ejecuta ante cada cambio y, además, todos los días a las
08:00 hora de Chile, porque una vulnerabilidad nueva se puede publicar sin que nadie toque el
repositorio.

En integración continua, las pruebas de extremo a extremo se reintentan hasta dos veces. Una prueba
que falla y después pasa al reintentarla se informa como **inestable** (*flaky*), y el pipeline
falla igual: una prueba inestable no se acepta, se corrige.

Los resultados se ven en la pestaña **Actions** del repositorio.

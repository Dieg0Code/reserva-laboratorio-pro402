import { expect, test } from "@playwright/test";

test.beforeEach(async ({ request }) => {
  await request.post("/_prueba/reiniciar");
});

test("si la red falla, el botón vuelve a quedar disponible", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("listitem")).toHaveCount(8);
  await page.route("**/reservas", (ruta) => ruta.abort());

  await page.getByLabel("Nombre").fill("Ana Rivas");
  await page.getByLabel("RUT").fill("11.111.111-1");
  await page.getByLabel("Correo electrónico").fill("ana.rivas@ejemplo.cl");
  await page.getByLabel("Bloque", { exact: true }).selectOption("4");
  await page.getByLabel("Personas").fill("12");
  await page.getByRole("button", { name: "Reservar" }).click();

  await expect(page.getByRole("button", { name: "Reservar" })).toBeEnabled();
});

test("en una pantalla de 320 píxeles no hay desplazamiento horizontal", async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 640 });
  await page.goto("/");
  await expect(page.getByRole("listitem")).toHaveCount(8);

  const ancho = await page.evaluate(() => document.documentElement.scrollWidth);

  expect(ancho).toBeLessThanOrEqual(320);
});

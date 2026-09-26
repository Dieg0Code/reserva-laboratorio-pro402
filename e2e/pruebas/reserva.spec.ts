import { expect, test } from "@playwright/test";

test.beforeEach(async ({ request }) => {
  await request.post("/_prueba/reiniciar");
});

test("una reserva completa se confirma en pantalla", async ({ page }) => {
  await page.goto("/");

  await page.getByLabel("Nombre").fill("Ana Rivas");
  await page.getByLabel("RUT").fill("11.111.111-1");
  await page.getByLabel("Correo electrónico").fill("ana.rivas@ejemplo.cl");
  await page.getByLabel("Bloque", { exact: true }).selectOption("4");
  await page.getByLabel("Personas").fill("12");
  await page.getByRole("button", { name: "Reservar" }).click();

  await expect(page.getByRole("status")).toContainText("Reserva confirmada");
});

test("si falta un dato, la pantalla dice cuál corregir", async ({ page }) => {
  await page.goto("/");

  await page.getByLabel("Nombre").fill("Ana Rivas");
  await page.getByLabel("RUT").fill("11.111.111-1");
  await page.getByLabel("Correo electrónico").fill("ana.rivas@ejemplo.cl");
  await page.getByLabel("Bloque", { exact: true }).selectOption("5");
  await page.getByRole("button", { name: "Reservar" }).click();

  await expect(page.getByRole("status")).toContainText("Personas");
});

import { expect, test, type Page } from "@playwright/test";

test.beforeEach(async ({ request }) => {
  await request.post("/_prueba/reiniciar");
});

async function reservarBloque4(page: Page) {
  await page.goto("/");
  await expect(page.getByRole("listitem")).toHaveCount(8);

  await page.getByLabel("Nombre").fill("Ana Rivas");
  await page.getByLabel("RUT").fill("11.111.111-1");
  await page.getByLabel("Correo electrónico").fill("ana.rivas@ejemplo.cl");
  await page.getByLabel("Bloque", { exact: true }).selectOption("4");
  await page.getByLabel("Personas").fill("12");
  await page.getByRole("button", { name: "Reservar" }).click();
}

test("tras reservar, el bloque 4 aparece tomado · espera una condición", async ({ page }) => {
  await reservarBloque4(page);

  const ficha = page.getByRole("listitem").filter({ hasText: "Bloque 4" });
  await expect(ficha).toContainText("Tomado");
});

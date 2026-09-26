import { expect, test } from "@playwright/test";

test.beforeEach(async ({ request }) => {
  await request.post("/_prueba/reiniciar");
});

test("una reserva se completa solo con el teclado", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("listitem")).toHaveCount(8);

  await page.keyboard.press("Tab");
  await page.keyboard.type("Ana Rivas");
  await page.keyboard.press("Tab");
  await page.keyboard.type("11.111.111-1");
  await page.keyboard.press("Tab");
  await page.keyboard.type("ana.rivas@ejemplo.cl");
  await page.keyboard.press("Tab");
  await page.keyboard.press("ArrowDown");
  await page.keyboard.press("ArrowDown");
  await page.keyboard.press("ArrowDown");
  await page.keyboard.press("Tab");
  await page.keyboard.type("12");
  await page.keyboard.press("Enter");

  await expect(page.getByRole("status")).toContainText("Reserva confirmada");
  await expect(page.getByRole("listitem").filter({ hasText: "Bloque 4" })).toContainText("Tomado");
});

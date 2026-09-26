import AxeBuilder from "@axe-core/playwright";
import { expect, test } from "@playwright/test";

const PAUTAS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"];

test.beforeEach(async ({ request }) => {
  await request.post("/_prueba/reiniciar");
});

test("con un bloque tomado, la página no tiene fallas de accesibilidad detectables", async ({ page, request }) => {
  await request.post("/reservas", {
    data: {
      nombre: "Ana Rivas",
      rut: "11.111.111-1",
      correo_electronico: "ana.rivas@ejemplo.cl",
      bloque: 4,
      personas: 12,
    },
  });
  await page.goto("/");
  await expect(page.getByRole("listitem").filter({ hasText: "Bloque 4" })).toContainText("Tomado");

  const resultado = await new AxeBuilder({ page }).withTags(PAUTAS).analyze();

  expect(resultado.violations.map((v) => v.id)).toEqual([]);
});

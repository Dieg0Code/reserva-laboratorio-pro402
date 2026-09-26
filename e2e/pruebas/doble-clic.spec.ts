import { expect, test, type Page } from "@playwright/test";

test.beforeEach(async ({ request }) => {
  await request.post("/_prueba/reiniciar");
});

async function llenarBloque4(page: Page) {
  await page.goto("/");
  await expect(page.getByRole("listitem")).toHaveCount(8);
  await page.getByLabel("Nombre").fill("Ana Rivas");
  await page.getByLabel("RUT").fill("11.111.111-1");
  await page.getByLabel("Correo electrónico").fill("ana.rivas@ejemplo.cl");
  await page.getByLabel("Bloque", { exact: true }).selectOption("4");
  await page.getByLabel("Personas").fill("12");
}

test("un doble clic envía una sola solicitud de reserva", async ({ page }) => {
  await llenarBloque4(page);
  const solicitudes: string[] = [];
  page.on("request", (r) => {
    if (r.method() === "POST" && r.url().endsWith("/reservas")) solicitudes.push(r.url());
  });

  await page.getByRole("button", { name: "Reservar" }).dblclick();
  await expect(page.getByRole("status")).not.toBeEmpty();

  expect(solicitudes).toHaveLength(1);
});

test("tras un doble clic, el mensaje dice lo que realmente pasó", async ({ page }) => {
  await llenarBloque4(page);

  await page.getByRole("button", { name: "Reservar" }).dblclick();
  await expect(page.getByRole("listitem").filter({ hasText: "Bloque 4" })).toContainText("Tomado");

  await expect(page.getByRole("status")).toContainText("Reserva confirmada");
});

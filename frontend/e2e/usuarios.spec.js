import { test, expect } from "@playwright/test";

test("admin puede crear usuario desde el frontend", async ({ page }) => {
  const usuarioNuevo = `usuarioe2e${Date.now()}`;

  await page.goto("/login");

  await page.getByPlaceholder("Usuario").fill("admin");
  await page.getByPlaceholder("Clave").fill("admin");
  await page.getByRole("button", { name: "Ingresar" }).click();

  await expect(page).toHaveURL(/dashboard/);

  await page.goto("/usuarios");

  await page.getByRole("button", { name: "Nuevo usuario" }).click();

  const inputsTexto = page.locator('input[type="text"]');

  await inputsTexto.nth(0).fill("Usuario E2E");
  await inputsTexto.nth(1).fill(usuarioNuevo);
  await page.locator('input[type="password"]').fill("1234");

  await page.locator("select").selectOption({ label: "usuario" });

  await page.getByRole("button", { name: "Guardar" }).click();

  await expect(page.locator("table")).toContainText(usuarioNuevo);
});
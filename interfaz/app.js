const formulario = document.querySelector("#formulario");
const mensaje = document.querySelector("#mensaje");
const grilla = document.querySelector("#bloques");

async function cargarBloques() {
  const respuesta = await fetch("/bloques");
  const { tomados } = await respuesta.json();
  grilla.innerHTML = "";
  for (let bloque = 1; bloque <= 8; bloque++) {
    const tomado = tomados.includes(bloque);
    const ficha = document.createElement("li");
    ficha.className = tomado ? "ficha tomada" : "ficha libre";
    ficha.innerHTML = `<span>Bloque ${bloque}</span><span class="estado">${tomado ? "Tomado" : "Libre"}</span>`;
    grilla.append(ficha);
  }
}

formulario.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const boton = formulario.querySelector("button");
  if (boton.disabled) return;
  boton.disabled = true;
  const datos = Object.fromEntries(new FormData(formulario));

  try {
    const respuesta = await fetch("/reservas", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(datos),
    });
    const cuerpo = await respuesta.json();

    if (respuesta.ok) {
      mensaje.className = "mensaje exito";
      mensaje.textContent = `Reserva confirmada. ${cuerpo.comprobante}`;
      formulario.reset();
      cargarBloques();
    } else {
      mensaje.className = "mensaje error";
      mensaje.textContent = Array.isArray(cuerpo.detail)
        ? cuerpo.detail.map(textoDelError).join(" ")
        : cuerpo.detail;
    }
  } catch {
    mensaje.className = "mensaje error";
    mensaje.textContent = "No se pudo conectar con el sistema. Intenta de nuevo.";
  } finally {
    boton.disabled = false;
  }
});

function textoDelError(error) {
  const nombreDelCampo = error.loc.at(-1);
  const campo = formulario.elements.namedItem(nombreDelCampo);
  const etiqueta = campo?.labels?.[0]?.textContent ?? nombreDelCampo;
  return `Revisa el campo ${etiqueta}.`;
}

cargarBloques();

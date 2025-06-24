document.addEventListener("DOMContentLoaded", async () => {
  const params = new URLSearchParams(window.location.search);
  const ci = params.get("ci");
  if (!ci) return;

  try {
    const response = await fetch(`http://localhost:8000/parseos/nino/?ci=${ci}&tipo=control`);
    const data = await response.json();
    const controles = data.control || [];

    const contenedor = document.querySelector(".health-cards-mobile");
    const boton = contenedor.querySelector(".add-health-card-btn");
    let indice = 0;

    const renderTarjeta = (control) => {
      const tarjeta = document.createElement("div");
      tarjeta.classList.add("health-card");

      tarjeta.innerHTML = `
        <div class="health-card-row"><label>Fecha</label><input type="text" value="${formatearFecha(control.fecha)}" readonly></div>
        <div class="health-card-row"><label>Edad</label><input type="text" value="${control.edad}" readonly></div>
        <div class="health-card-row"><label>Peso (kg)</label><input type="text" value="${control.peso}" readonly></div>
        <div class="health-card-row"><label>Talla (cm)</label><input type="text" value="${control.talla}" readonly></div>
        <div class="health-card-row"><label>PC (cm)</label><input type="text" value="${control.pc}" readonly></div>
        <div class="health-card-row"><label>Alimentación PD</label><input type="text" value="${control.alimentacion_pd ? '✔' : '✘'}" readonly></div>
        <div class="health-card-row"><label>Alimentación PPL</label><input type="text" value="${control.alimentacion_ppl ? '✔' : '✘'}" readonly></div>
        <div class="health-card-row"><label>Hierro Vit. D</label><input type="text" value="${control.hierro_vit_d ? '✔' : '✘'}" readonly></div>
        <div class="health-card-row"><label>Circunferencia de cintura</label><input type="text" value="${control.circunferencia_cintura}" readonly></div>
        <div class="health-card-row"><label>IMC</label><input type="text" value="${control.imc}" readonly></div>
        <div class="health-card-row"><label>PAS</label><input type="text" value="${control.pas}" readonly></div>
        <div class="health-card-row"><label>PAD</label><input type="text" value="${control.pad}" readonly></div>
        <div class="health-card-row"><label>Fecha próxima consulta</label><input type="text" value="${formatearFecha(control.fecha_proxima_consulta)}" readonly></div>
      `;

      contenedor.insertBefore(tarjeta, boton);
    };

    if (controles.length > 0) renderTarjeta(controles[indice++]);

    boton.addEventListener("click", () => {
      if (indice < controles.length) {
        renderTarjeta(controles[indice++]);
      } else {
        boton.disabled = true;
        boton.textContent = "(No hay más controles)";
      }
    });

    function formatearFecha(fechaISO) {
      if (!fechaISO) return "";
      const [a, m, d] = fechaISO.split("-");
      return `${d}/${m}/${a}`;
    }
  } catch (error) {
    console.error("❌ Error al cargar controles:", error);
  }
});

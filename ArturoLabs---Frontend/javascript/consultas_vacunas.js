document.addEventListener("DOMContentLoaded", async () => {
  const params = new URLSearchParams(window.location.search);
  const ci = params.get("ci");
  if (!ci) return alert("Falta la cédula en la URL");

  try {
    const response = await fetch(`http://localhost:8000/parseos/nino/?ci=${ci}&tipo=control`);
    const data = await response.json();
    const controles = data.control || [];

    const tbody = document.querySelector("#healthTable tbody");
    tbody.innerHTML = ""; // Limpiamos cualquier fila placeholder

    controles.forEach(control => {
      const tr = document.createElement("tr");

      tr.innerHTML = `
        <td><input type="text" value="${formatearFecha(control.fecha)}" readonly></td>
        <td><input type="text" value="${control.edad ?? ''}" readonly></td>
        <td><input type="text" value="${control.peso ?? ''}" readonly></td>
        <td><input type="text" value="${control.talla ?? ''}" readonly></td>
        <td><input type="text" value="${control.pc ?? ''}" readonly></td>
        <td><input type="text" value="${control.alimentacion_pd ? '✔' : '✘'}" readonly></td>
        <td><input type="text" value="${control.alimentacion_ppl ? '✔' : '✘'}" readonly></td>
        <td><input type="text" value="${control.hierro_vit_d ? '✔' : '✘'}" readonly></td>
        <td><input type="text" value="${control.circunferencia_cintura ?? ''}" readonly></td>
        <td><input type="text" value="${control.imc ?? ''}" readonly></td>
        <td><input type="text" value="${control.pas ?? ''}" readonly></td>
        <td><input type="text" value="${control.pad ?? ''}" readonly></td>
        <td><input type="text" value="${formatearFecha(control.fecha_proxima_consulta)}" readonly></td>
      `;

      tbody.appendChild(tr);
    });

  } catch (error) {
    console.error("❌ Error al cargar controles:", error);
    alert("No se pudo cargar la información del niño.");
  }

  function formatearFecha(fechaISO) {
    if (!fechaISO) return "";
    const [a, m, d] = fechaISO.split("-");
    return `${d}/${m}/${a}`;
  }
});

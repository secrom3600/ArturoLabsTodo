document.addEventListener("DOMContentLoaded", async () => {
  console.log("📦 Script vacunas.js cargado");
  const params = new URLSearchParams(window.location.search);
  const ci = params.get("ci");
  if (!ci) return;

  

  try {
    const response = await fetch(`http://localhost:8000/parseos/nino/?ci=${ci}&tipo=vacunas`);
    const data = await response.json();
    

    const vacunasLista = data.vacunas || [];
    

    const edadesMeses = [0, 2, 4, 6, 12, 15, 21];
    const edadesAnios = [5, 11];

    const edadCercana = (lista, edadRef) => {
      return lista.reduce((prev, curr) =>
        Math.abs(curr - edadRef) < Math.abs(prev - edadRef) ? curr : prev
      );
    };

    const vacunaMap = {
      "bcg": "BCG",
      "pentavalente": "Pentavalente*",
      "polio": "Polio",
      "srp": "Sarampión-rubeola-paperas**",
      "varicela": "Varicela",
      "neumococo_13v": "Neumococo 13 V",
      "hepatitis_a": "Hepatitis A",
      "triple_bacteriana_dpt": "Triple bacteriana (DPT)",
      "triple_bacteriana_dpat": "Triple bacteriana acelular (dpaT)",
      "vph": "Virus papiloma humano (VPH)",
      "anti_influenza": "Anti-influenza***"
    };

    const tabla = document.querySelector("#vaccineTable-full");
    if (!tabla) {
      console.warn("⚠️ Tabla 'vaccineTable-full' no encontrada.");
      return;
    }

    vacunasLista.forEach((registro, index) => {
      

      const edadMeses = parseInt(registro.edad_meses ?? 0);
      const edadAnios = parseInt(registro.edad_anios ?? 0);
      const edadTotalMeses = edadMeses || (edadAnios * 12);

      const esEdadEnAnios = edadTotalMeses >= 60;
      const columna = esEdadEnAnios
        ? 7 + edadesAnios.indexOf(edadCercana(edadesAnios, edadTotalMeses / 12))
        : edadesMeses.indexOf(edadCercana(edadesMeses, edadTotalMeses));

      for (const key in vacunaMap) {
        const valor = registro[key];
        
        if (valor === true || valor === "true") {
          const label = vacunaMap[key];
          

          const fila = [...tabla.querySelectorAll("tbody tr")].find(tr => {
            const th = tr.querySelector(".vaccine-header");
            return th?.textContent.trim() === label;
          });

          if (fila && columna >= 0) {
            const celdas = fila.querySelectorAll("td");
            const celda = celdas[columna + 1]; // +1 para saltear nombre de vacuna
            if (celda) {
              celda.classList.add("selected");
            }
          }
        }
      }
    });

  } catch (e) {
    console.error("❌ Error al cargar vacunas:", e);
  }
});

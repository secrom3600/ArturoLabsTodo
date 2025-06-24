document.addEventListener("DOMContentLoaded", async () => {
  console.log("📱 Script vacunas_mobile.js cargado");

  const params = new URLSearchParams(window.location.search);
  const ci = params.get("ci");
  if (!ci) return;

  try {
    const response = await fetch(`http://localhost:8000/parseos/nino/?ci=${ci}&tipo=vacunas`);
    const data = await response.json();
    const listaVacunas = data.vacunas || [];

    console.log("📦 Lista completa de vacunas:", listaVacunas);

    const vacunaMap = {
      bcg: "BCG",
      pentavalente: "Pentavalente*",
      polio: "Polio",
      srp: "Sarampión-rubeola-paperas**",
      varicela: "Varicela",
      neumococo_13v: "Neumococo 13 V",
      hepatitis_a: "Hepatitis A",
      triple_bacteriana_dpt: "Triple bacteriana (DPT)",
      triple_bacteriana_dpat: "Triple bacteriana acelular (dpaT)",
      vph: "Virus papiloma humano (VPH)",
      anti_influenza: "Anti-influenza***"
    };

    const edadesMeses = [0, 2, 4, 6, 12, 15, 21];
    const edadesAnios = [5, 11];

    const edadCercana = (lista, edadRef) => {
      return lista.reduce((prev, curr) =>
        Math.abs(curr - edadRef) < Math.abs(prev - edadRef) ? curr : prev
      );
    };

    listaVacunas.forEach((registro, index) => {
      const edadMeses = parseInt(registro.edad_meses ?? 0);
      const edadAnios = parseInt(registro.edad_anios ?? 0);
      const edadTotalMeses = edadMeses || (edadAnios * 12);

      const esEnAnios = edadTotalMeses >= 60;
      const edadUsada = esEnAnios
        ? edadCercana(edadesAnios, edadTotalMeses / 12)
        : edadCercana(edadesMeses, edadTotalMeses);

      const tabla = document.querySelector(esEnAnios ? "#vaccineTable-anos" : "#vaccineTable-meses");
      if (!tabla) return;

      for (const key in vacunaMap) {
        const nombreTabla = vacunaMap[key];
        const valor = registro[key];

        if (valor === true || valor === "true") {
          const fila = [...tabla.querySelectorAll("tbody tr")].find(tr => {
            const th = tr.querySelector(".vaccine-header");
            return th?.textContent.trim() === nombreTabla;
          });

          if (fila) {
            const columnas = fila.querySelectorAll("td");
            const indexCol = esEnAnios
              ? edadesAnios.indexOf(edadUsada) + 1
              : edadesMeses.indexOf(edadUsada) + 1;

            const celda = columnas[indexCol];
            if (celda) celda.classList.add("selected");
          }
        }
      }
    });
  } catch (e) {
    console.error("❌ Error al cargar vacunas:", e);
  }
});

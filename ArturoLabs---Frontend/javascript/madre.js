document.addEventListener("DOMContentLoaded", async () => {
  const params = new URLSearchParams(window.location.search);
  const ci = params.get("ci");
  if (!ci) return alert("Falta la cédula del niño en la URL");

  try {
    const response = await fetch(`http://localhost:8000/parseos/nino/?ci=${ci}&tipo=embarazo`);
    const data = await response.json();
    const info = data.embarazo?.[0];
    if (!info) return alert("No se encontró información de embarazo para esta cédula");

    // Rellenar campos correctamente
    marcarRadio("multiple", info.embarazo_multiple);
    document.getElementById("nro_controles").value = info.num_controles_prenatales || "";

    marcarRadio("its", info.its);
    document.getElementById("resultado_its").value = info.resultado || "";
    document.getElementById("tratamiento_its").value = info.tratamiento || "";

    marcarRadio("vaginal", info.tp_vaginal);
    marcarRadio("cesarea", info.tp_cesarea);
    marcarRadio("institucional", info.tp_institucional);
    document.getElementById("otro_tipo").value = info.otro_tipo_parto || "";

    marcarRadio("acomp", info.acompanamiento_parto);
    document.getElementById("acomp_nom").value = info.nombre_acompanante || "";
    document.getElementById("acomp_ap").value = info.apellido_acompanante || "";
    document.getElementById("edad_gestacional").value = info.edad_gestacional_semanas || "";
    document.getElementById("peso_nacer").value = info.peso_al_nacer_gramos || "";

  } catch (err) {
    console.error("❌ Error al cargar datos del embarazo:", err);
    alert("Error al cargar datos del embarazo");
  }

  function marcarRadio(nombreCampo, valorBool) {
    const valor = valorBool ? "si" : "no";
    const radio = document.querySelector(`input[name="${nombreCampo}"][value="${valor}"]`);
    if (radio) radio.checked = true;
  }
});

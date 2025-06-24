document.addEventListener("DOMContentLoaded", async () => {
  const params = new URLSearchParams(window.location.search);
  const ci = params.get("ci");
  if (!ci) return;

  try {
    const res = await fetch(`http://127.0.0.1:8000/api/control/${ci}/`);
    const data = await res.json();

    const img = document.getElementById("graficoIMC");
    if (img && data.imc_edad_graph) {
      img.src = data.imc_edad_graph;
      img.alt = "Gráfico IMC cargado";
    }
  } catch (e) {
    console.error("❌ Error al cargar gráfico IMC:", e);
  }
});

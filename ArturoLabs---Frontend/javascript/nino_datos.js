const token = localStorage.getItem("accessToken");
const headers = {
  Authorization: `Bearer ${token}`,
};

document.addEventListener("DOMContentLoaded", async () => {
  const params = new URLSearchParams(window.location.search);
  const ci = params.get("ci");

  if (!ci) {
    alert("Falta la cédula del niño en la URL");
    return;
  }

  try {
    // 1. Obtener datos del niño desde parseo XML
    const responseNino = await fetch(`http://localhost:8000/parseos/nino/?ci=${ci}&tipo=nino`);
    const dataNino = await responseNino.json();
    const infoNino = dataNino.nino?.[0];

    if (!infoNino) {
      alert("No se encontraron datos del niño");
      return;
    }

    // Rellenar los campos del niño
    document.getElementById("nombres").value = infoNino.nombres || "";
    document.getElementById("apellidos").value = infoNino.apellidos || "";
    document.getElementById("etnia").value = infoNino.etnia_raza || "";
    document.getElementById("sexo").value = infoNino.sexo || "";
    document.getElementById("fecha_nacimiento").value = infoNino.fecha_nacimiento || "";
    document.getElementById("codigo_identidad").value = infoNino.id_nino || "";
    document.getElementById("domicilio").value = infoNino.domicilio || "";
    document.getElementById("telefono").value = infoNino.telefono || "";
    document.getElementById("servicio_salud").value = infoNino.servicio_salud || "";
    document.getElementById("emergencia_movil").value = infoNino.emergencia_movil || "";

    // 2. Obtener tutorci y tutordosci desde la base de datos
    const responseCI = await fetch(`http://localhost:8000/api/nino/${ci}/`);
    const ninoDB = await responseCI.json();

    const ci1 = ninoDB.tutorci;
    const ci2 = ninoDB.tutordosci;

    // 3. Obtener datos del primer tutor
    const respTutor1 = await fetch(`http://localhost:8000/api/tutor/${ci1}`);
    const tutor1 = await respTutor1.json();

    document.getElementById("c1_nombres").value = tutor1.nombre || "";
    document.getElementById("c1_apellidos").value = tutor1.apellido || "";
    document.getElementById("c1_cedula").value = tutor1.ci || "";
    document.getElementById("c1_fecha_nac").value = tutor1.fec_nac || "";
    document.getElementById("c1_telefono_contacto").value = tutor1.telefono || "";
    console.log("Tutor 1:", tutor1);

    // 4. Si hay segundo tutor
    if (ci2) {
      const respTutor2 = await fetch(`http://localhost:8000/api/tutor/${ci2}`);
      const tutor2 = await respTutor2.json();

      document.getElementById("c2_nombres").value = tutor2.nombre || "";
      document.getElementById("c2_apellidos").value = tutor2.apellido || "";
      document.getElementById("c2_cedula").value = tutor2.ci || "";
      document.getElementById("c2_fecha_nac").value = tutor2.fec_nac || "";
      document.getElementById("c2_telefono_contacto").value = tutor2.telefono || "";
      console.log("Tutor 2:", tutor2);
    }

  } catch (error) {
    console.error("❌ Error al cargar los datos:", error);
    alert("Error al cargar los datos del niño y tutores");
  }
});
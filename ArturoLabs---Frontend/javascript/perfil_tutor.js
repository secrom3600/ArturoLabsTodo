const API_URL = "http://localhost:8000/api";

import { fetchConToken } from "./auth.js";

export async function cargarPerfilTutor() {
  try {
    const response = await fetchConToken(`${API_URL}/tutorDatosAll/`);
    if (!response.ok) {
      throw new Error("No se pudo obtener la información del tutor.");
    }

    const tutor = await response.json();

    document.getElementById("tutorNombres").textContent = tutor.nombre || "—";
    document.getElementById("tutorApellidos").textContent = tutor.apellido || "—";
    document.getElementById("tutorCI").textContent = tutor.ci || "—";
    document.getElementById("tutorNacionalidad").textContent = tutor.nacionalidad || "—";
    document.getElementById("tutorFechaNac").textContent = tutor.fec_nac || "—";
    document.getElementById("tutorSexo").textContent = tutor.sexo || "—";
    document.getElementById("tutorDireccion").textContent = tutor.direccion || "—";
    document.getElementById("tutorLocalidad").textContent = tutor.localidad || "—";
    document.getElementById("tutorEmail").textContent = tutor.email || "—";
    document.getElementById("tutorTelefono").textContent = tutor.telefono || "—";

  } catch (error) {
    console.error("❌ Error al cargar perfil del tutor:", error);
  }
}

export async function cargarTablaHijos() {
  const tbody = document.getElementById("tablaHijosBody");
  if (!tbody) return;

  try {
    const response = await fetchConToken(`${API_URL}/hijosTutor/`);
    if (!response.ok) throw new Error("No se pudo obtener la información de los hijos.");

    const hijos = await response.json();
    tbody.innerHTML = "";

    if (hijos.length === 0) {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td colspan="5" style="text-align:center; padding: 20px; font-style: italic; background-color: #eaf6fb; color: #555;">
                        (No hay niños registrados)
                      </td>`;
      tbody.appendChild(tr);
      return;
    }

    hijos.forEach(hijo => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td data-label="Nombres">${hijo.nombre}</td>
        <td data-label="Apellidos">${hijo.apellido}</td>
        <td data-label="Cédula de Identidad">${hijo.ci}</td>
        <td data-label="Fecha de Nacimiento">${hijo.fecha_nac || "—"}</td>
        <td data-label="Acciones" class="actions-cell">
          <a href="form_datos.html?ci=${hijo.ci}">Ver Carné</a> |
          <a href="consultas_vacunas.html?ci=${hijo.ci}">Consultas y Vacunas</a> |
          <a href="form_madre.html?ci=${hijo.ci}">Ver Madre</a>
        </td>
      `;
      tbody.appendChild(tr);
    });

    const trFinal = document.createElement("tr");
    trFinal.innerHTML = `<td colspan="5" style="text-align:center; padding: 20px; font-style: italic; background-color: #eaf6fb; color: #555;">
                          (Fin de la lista)
                        </td>`;
    tbody.appendChild(trFinal);

    const selectChildLinks = tbody.querySelectorAll('.select-child-link');
    selectChildLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();

        const childCI = e.target.dataset.childCi;
        const childName = e.target.dataset.childName;
        const childLastName = e.target.dataset.childLastname;

        localStorage.setItem('selectedChildCI', childCI);
        localStorage.setItem('selectedChildName', `${childName} ${childLastName}`);

        updateMainMenu(); 

        window.location.href = `form_datos.html?ci=${childCI}`;
      });
    });

  } catch (error) {
    console.error("❌ Error al cargar tabla de hijos:", error);
  }
}

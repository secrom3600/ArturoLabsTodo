const API_URL = "http://localhost:8000/api"; // Ajusta la URL según sea necesario

export async function login(ci, password) {
  console.log("➡️ login() llamado con", ci, password);
  try {
    const response = await fetch(`${API_URL}/token/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ci, password })
    });

    const data = await response.json();
    console.log("Login response:", data);

    if (response.ok && data.access && data.refresh) {
      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);
      return { success: true, message: data.message };
    } else {
      return { success: false, message: data.message || "Error en login" };
    }
  } catch (error) {
    console.error("Error durante login:", error);
    return { success: false, message: "Fallo en la conexión" };
  }
}


export function getAccessToken() {
  return localStorage.getItem("access");
}

export async function refreshToken() {
  try {
    const response = await fetch(`${API_URL}/token/refresh/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh: localStorage.getItem("refresh") }),
    });

    if (response.ok) {
      const data = await response.json();
      localStorage.setItem("access", data.access);
      return true;
    } else {
      return false;
    }
  } catch (error) {
    console.error("Error al refrescar token:", error);
    return false;
  }
}

export function logout() {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
}

// Nuevo: fetchConToken que renueva el access token si expira
export async function fetchConToken(url, options = {}) {
  const accessToken = getAccessToken();

  const headers = {
    ...options.headers,
    Authorization: `Bearer ${accessToken}`,
    "Content-Type": "application/json",
  };

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    const refreshed = await refreshToken();
    if (refreshed) {
      const newAccessToken = getAccessToken();
      const retryHeaders = {
        ...options.headers,
        Authorization: `Bearer ${newAccessToken}`,
        "Content-Type": "application/json",
      };

      return fetch(url, {
        ...options,
        headers: retryHeaders,
      });
    } else {
      logout();
      throw new Error("Sesión expirada. Por favor, iniciá sesión nuevamente.");
    }
  }

  return response;
}


export async function cargarHijos() {
  const hijosContainer = document.querySelector(".dropdown-body");
  if (!hijosContainer) {
    console.warn("⚠️ No se encontró el contenedor de hijos: .dropdown-body");
    return;
  }

  try {
    const response = await fetchConToken("http://localhost:8000/api/hijos/");
    if (!response.ok) {
      throw new Error("No se pudo obtener la información de los hijos.");
    }

    const hijos = await response.json();
    hijosContainer.innerHTML = "";

    if (hijos.length === 0) {
      hijosContainer.innerHTML = "<li>No se encontraron hijos registrados.</li>";
      return;
    }

    const maxInicial = 3;

    hijos.forEach((hijo, index) => {
      const li = document.createElement("li");
      li.classList.add("child");

      if (index >= maxInicial) {
        li.style.display = "none";
        li.classList.add("extra-child");
      }

      li.innerHTML = `
        <strong>${hijo.full_name}</strong>
        <span>CI: ${hijo.ci} - Edad: ${hijo.edad} años</span>
      `;

      hijosContainer.appendChild(li);
    });

    if (hijos.length > maxInicial) {
      const verTodosBtn = document.createElement("a");
      verTodosBtn.href = "#";
      verTodosBtn.id = "verTodosBtn";
      verTodosBtn.textContent = "Ver todos";

      verTodosBtn.addEventListener("click", (e) => {
        e.preventDefault();
        document.querySelectorAll(".extra-child").forEach((li) => {
          li.style.display = "list-item";
        });
        verTodosBtn.remove(); // Ocultar el enlace una vez mostrado
      });

      hijosContainer.appendChild(verTodosBtn);
    }

  } catch (error) {
    console.error("❌ Error al cargar hijos:", error);
    hijosContainer.innerHTML = "<li>Error al cargar hijos.</li>";
  }
}

export async function cargarTutor() {
  const header = document.querySelector(".dropdown-header");
  if (!header) {
    console.warn("⚠️ No se encontró el contenedor del tutor: .dropdown-header");
    return;
  }

  try {
    const response = await fetchConToken("http://localhost:8000/api/tutorDatos/");
    if (!response.ok) {
      throw new Error("No se pudo obtener la información del tutor.");
    }

    const tutor = await response.json();

    header.innerHTML = `
      <h4>${tutor.full_name}</h4>
      <p>CI: ${tutor.ci}</p>
    `;
  } catch (error) {
    console.error("❌ Error al cargar tutor:", error);
    header.innerHTML = `
      <h4>Error al cargar</h4>
      <p>CI: —</p>
    `;
  }
}
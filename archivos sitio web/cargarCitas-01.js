async function cargarCitas(email, tipoUsuario) {
    try {
        const apiUrl = `https://4ikw2d7fph.execute-api.us-east-1.amazonaws.com/prod/citas`;

        // Construir la URL con parámetros
        const urlConParametros = `${apiUrl}?email=${encodeURIComponent(email)}&tipo=${encodeURIComponent(tipoUsuario)}`;

        const response = await fetch(urlConParametros, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
        });

        if (!response.ok) {
            throw new Error(`Error en la respuesta del servidor: ${response.status}`);
        }

        // Parsear el JSON de la respuesta
        const data = await response.json();

        // Si el servidor envía `body` como string, parsearlo nuevamente
        const responseBody = typeof data.body === "string" ? JSON.parse(data.body) : data.body;

        if (responseBody.citas && responseBody.citas.length > 0) {
            mostrarCitasEnTabla(responseBody.citas);
        } else {
            console.error("No se encontraron citas.");
            alert("No tienes citas agendadas.");
        }
    } catch (error) {
        console.error("Error al cargar las citas:", error);
        alert("Hubo un problema al cargar las citas. Por favor, intenta de nuevo más tarde.");
    }
}

function mostrarCitasEnTabla(citas) {
    const tablaCuerpo = document.querySelector("#tabla-citas tbody");
    tablaCuerpo.innerHTML = ""; // Limpiar la tabla antes de agregar nuevas filas

    citas.forEach(cita => {
        const fila = document.createElement("tr");
        fila.innerHTML = `
            <td>${cita.id}</td>
            <td>${cita.email || sessionStorage.getItem('email')}</td>
            <td>${cita.fecha_cita}</td>
            <td>${cita.estado}</td>
            <td>
                <button class="btn btn-success btn-sm btn-estado" data-cita-id="${cita.id}" data-nuevo-estado="completada">Completar</button>
                <button class="btn btn-danger btn-sm btn-estado" data-cita-id="${cita.id}" data-nuevo-estado="cancelada">Cancelar</button>
            </td>
        `;
        tablaCuerpo.appendChild(fila);
    });
}



async function crearCita(email, fechaCita) {
    const apiUrl = "https://4ikw2d7fph.execute-api.us-east-1.amazonaws.com/prod/citas"; // Link del API Gateway

    const payload = {
        email: email,
        fecha_cita: fechaCita
    };

    try {
        const response = await fetch(apiUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            const data = await response.json();
            console.log("Cita creada exitosamente:", data.message);
            alert("¡Cita creada exitosamente!");
            window.location.reload();
        } else {
            const error = await response.json();
            console.error("Error al crear la cita:", error.message);
            alert("Error al crear la cita: " + error.message);
            window.location.reload();
        }
    } catch (err) {
        console.error("Error en la solicitud:", err);
        alert("Hubo un problema al crear la cita.");
    }
}

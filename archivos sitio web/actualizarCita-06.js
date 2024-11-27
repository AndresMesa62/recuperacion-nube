async function actualizarEstadoCita(citaId, nuevoEstado) {
    const apiUrl = "https://bj6enx5q7hgjnnxtqnwe6a5ms40nyguj.lambda-url.us-east-1.on.aws/";
    
    const data = {
        cita_id: citaId,
        estado: nuevoEstado
    };
    
    try {
        console.log("Enviando datos:", data); // Verifica qué datos estás enviando

        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const responseData = await response.json(); // Procesa la respuesta del servidor
        console.log("Respuesta del servidor:", responseData);

        if (!response.ok) {
            throw new Error(`Error en la solicitud: ${response.status}`);
        }

        console.log("Estado actualizado exitosamente:", data);

        // Recargar la página después de actualizar
        window.location.reload();
    } catch (error) {
        console.error("Error al actualizar el estado de la cita:", error);
        alert("No se pudo actualizar el estado de la cita. Por favor, inténtalo nuevamente.");
    }
}

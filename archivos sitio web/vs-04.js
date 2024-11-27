function saveData(user_data) {
    try {
        const now = new Date();

        // Guardar datos del usuario en sessionStorage
        sessionStorage.setItem('email', user_data.email);
        sessionStorage.setItem('role', user_data.tipo);
        sessionStorage.setItem('session-start-time', now.getTime());

        re() // Puedes descomentar esto si tienes otra lógica para continuar
    } catch (e) {
        console.error("Error al guardar en sessionStorage:", e);
    }
}

function vs(accessToken) {
    sessionStorage.clear(); // Limpiar la sesión actual

    // Construir la URL del API con el token como parámetro de consulta
    const apiUrl = `https://4ikw2d7fph.execute-api.us-east-1.amazonaws.com/prod/sesion?access_token=${encodeURIComponent(accessToken)}`;

    // Hacer la solicitud GET al API
    fetch(apiUrl, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => {
            // Verificar si la respuesta es válida
            if (!response.ok) {
                throw new Error(`Error en la respuesta del servidor: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Depuración: Verificar la respuesta completa
            console.log("Respuesta del servidor:", data);

            // Convertir el body en JSON (si es un string)
            let parsedBody;
            try {
                parsedBody = JSON.parse(data.body); // Convertir el body en objeto
            } catch (e) {
                console.error("Error al analizar la respuesta del body:", e);
                throw new Error("Formato inesperado en la respuesta del servidor.");
            }

            // Validar si el token es válido y guardar datos
            if (parsedBody.message === "Validación exitosa" && parsedBody.user_info) {
                saveData(parsedBody.user_info);
            } else {
                console.error("Token inválido o datos incompletos.");
                redirectToLogin();
            }
        })
        .catch(err => {
            console.error("Error durante la validación:", err);
            redirectToLogin(); // Redirigir al login en caso de error
        });
}


function redirectToLogin() {
    console.log("Redirigiendo al login...");
    window.location.href = "https://us-east-1wvajz8fth.auth.us-east-1.amazoncognito.com/login?client_id=qdu1h0lss968s250s83digj89&redirect_uri=https://d3cwfcl9tm8fda.cloudfront.net&response_type=token&scope=email+openid";
}

function se() {
    const sessionStartTime = sessionStorage.getItem('session-start-time');
    const email = sessionStorage.getItem('email'); // Verifica si hay un email almacenado
    const role = sessionStorage.getItem('role');  // Verifica si hay un rol almacenado
    const now = new Date().getTime();

    // Si no hay sesión iniciada o faltan datos esenciales, redirigir al inicio de sesión
    if (!sessionStartTime || !email || !role) {
        sessionStorage.clear();
        redirectToLogin();
        return;
    }

    // Verificar si la sesión ha expirado (24 horas = 86400000 ms)
    if ((now - sessionStartTime) > 86400000) {
        sessionStorage.clear();
        redirectToLogin();
        return;
    }
}

function redirectToLogin() {
    window.location.href = "https://us-east-1wvajz8fth.auth.us-east-1.amazoncognito.com/login?client_id=qdu1h0lss968s250s83digj89&redirect_uri=https://d3cwfcl9tm8fda.cloudfront.net&response_type=token&scope=email+openid";
}

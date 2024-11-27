function re() {

    const role = sessionStorage.getItem('role');
    const email = sessionStorage.getItem('email');

    // Verificar si el nombre y el rol están presentes
    if (role && email) {
        
        if (role === 'default') {
            window.location.href = "menu.html";
        }else if (role === 'admin') {
            window.location.href = "menu.html";
        } else {
            redirectToLogin()
        }
    } else {
        console.log("Nombre o rol no están presentes. No se hace ninguna redirección.");
    }
}

function redirectToLogin() {
    window.location.href = "https://us-east-1wvajz8fth.auth.us-east-1.amazoncognito.com/login?client_id=qdu1h0lss968s250s83digj89&redirect_uri=https://d3cwfcl9tm8fda.cloudfront.net&response_type=token&scope=email+openid";
}

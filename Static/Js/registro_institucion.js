document.addEventListener('DOMContentLoaded', function () {
    // --- Funcionalidad para mostrar/ocultar contraseña ---
    const togglePasswordButton = document.querySelector('.toggle-password');
    // La función togglePassword se define aquí para que esté disponible en el listener.
    // No es necesario adjuntarla con addEventListener si se usa onclick en el HTML,
    // pero es mejor práctica mantener todo el JS aquí.
    // El HTML ya tiene onclick="togglePassword()", pero lo ideal sería quitarlo
    // y manejarlo aquí. Por ahora, lo dejamos para no romper la funcionalidad existente.
    if (togglePasswordButton) {
        // El HTML ya tiene un onclick, así que esta línea es redundante.
        // togglePasswordButton.addEventListener('click', togglePassword);
    }
    
    // Hacemos la función global para que el `onclick` del HTML la encuentre.
    window.togglePassword = function() {
        const passwordInput = document.getElementById('password');
        const eyeIcon = document.getElementById('eye-icon');

        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            eyeIcon.classList.remove('fa-eye-slash');
            eyeIcon.classList.add('fa-eye');
        } else {
            passwordInput.type = 'password';
            eyeIcon.classList.remove('fa-eye');
            eyeIcon.classList.add('fa-eye-slash');
        }
    }

    // --- Validación para requerir al menos un checkbox de participación ---
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function (event) {
            const checkboxes = document.querySelectorAll('.checkbox-group input[type="checkbox"]');
            const isChecked = Array.from(checkboxes).some(checkbox => checkbox.checked);

            if (!isChecked) {
                event.preventDefault(); // Previene el envío del formulario
                alert('Por favor, selecciona al menos un área de participación activa.'); // Muestra una alerta
                checkboxes[0].focus(); // Enfoca el primer checkbox para guiar al usuario
            }
        });
    }

    // --- Validación de correo electrónico ---
    // Hacemos la función global para que el `onblur` del HTML la encuentre.
    window.validarCorreo = function(email) {
        const expReg = /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;
        const esValido = expReg.test(email);
       
        if (email && !esValido) { // Solo muestra la alerta si hay texto y no es válido.
            alert("El correo no es válido, por favor ingrese un correo válido.");
            // Opcional: enfocar el campo de nuevo si es inválido
            const emailInput = document.getElementById('email');
            if (emailInput) {
                emailInput.focus();
            }
        }
    };

    // --- Validación de Contraseña ---
    const passwordInput = document.getElementById('password');

    if (passwordInput) {
        passwordInput.addEventListener('blur', function() {
            const password = this.value;
            if (password && !validarContraseña(password)) {
                alert('La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial que son los siguientes: !@#$%^&*._-');
            }
        });
    }

    function validarContraseña(password) {
        // La contraseña debe tener al menos 8 caracteres, una minúscula, una mayúscula, un número y un caracter especial.
        const expReg = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*._-])[A-Za-z\d!@#$%^&*._-]{8,}$/;
        return expReg.test(password);
    }

    function validarNIT(nit) {
        // Expresión regular para un NIT colombiano: 9 o 10 dígitos, opcionalmente con guion y dígito de verificación.
        const expRegNIT = /^\d{9,11}(?:-\d{1})?$/;
        return expRegNIT.test(nit);
    }

    // --- Validación de NIT ---
    const nitInput = document.getElementById('nit');
    if (nitInput) {
        nitInput.addEventListener('blur', function() {
            const nit = this.value;
            if (nit && !validarNIT(nit)) {
                alert('El NIT no es válido. Debe tener 9 o 10 dígitos, opcionalmente seguido de un guion y el dígito de verificación.');
            }
        });
    }

});
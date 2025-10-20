document.addEventListener('DOMContentLoaded', function () {
    // --- Funcionalidad para mostrar/ocultar contraseña ---
    const togglePasswordButton = document.querySelector('.toggle-password');

    // Hacemos la función global para que el `onclick` del HTML la encuentre por ahora.
    // Lo ideal sería manejar el evento 'click' aquí directamente.
    window.togglePassword = function() {
        const passwordInput = document.getElementById('contrasena');
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

    // --- Validación de correo electrónico ---
    const emailInput = document.getElementById('correo');
    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            validarCorreo(this.value);
        });
    }

    function validarCorreo(email) {
        const expReg = /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;
        const esValido = expReg.test(email);
       
        if (email && !esValido) { // Solo muestra la alerta si hay texto y no es válido.
            alert("El correo no es válido, por favor ingrese un correo válido.");
            // Opcional: enfocar el campo de nuevo si es inválido
            if (emailInput) {
                emailInput.focus();
            }
        }
    }

    // --- Validación de Contraseña ---
    const passwordInput = document.getElementById('contrasena');
    if (passwordInput) {
        passwordInput.addEventListener('blur', function() {
            const password = this.value;
            if (password && !validarContraseña(password)) {
                alert('La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial: !@#$%^&*._-');
            }
        });
    }

    function validarContraseña(password) {
        // La contraseña debe tener al menos 8 caracteres, una minúscula, una mayúscula, un número y un caracter especial.
        const expReg = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*._-])[A-Za-z\d!@#$%^&*._-]{8,}$/;
        return expReg.test(password);
    }

    // --- Validación para requerir al menos un checkbox ---
    const form = document.getElementById('investorForm');
    if (form) {
        form.addEventListener('submit', function (event) {
            // Validación para 'Etapas de los proyectos'
            const etapasCheckboxes = document.querySelectorAll('input[name="etapas"]');
            const etapaChecked = Array.from(etapasCheckboxes).some(checkbox => checkbox.checked);

            if (!etapaChecked) {
                event.preventDefault();
                alert('Por favor, selecciona al menos una etapa de proyecto en la que inviertes.');
                etapasCheckboxes[0].focus();
                return; // Detiene la validación si esta falla
            }

            // Validación para 'Áreas de interés'
            const areasCheckboxes = document.querySelectorAll('input[name="areas"]');
            const areaChecked = Array.from(areasCheckboxes).some(checkbox => checkbox.checked);

            if (!areaChecked) {
                event.preventDefault();
                alert('Por favor, selecciona al menos un área de interés.');
                areasCheckboxes[0].focus();
            }
        });
    }

    // --- Validación dinámica de Tipo y Número de Documento ---
    const tipoDocumentoSelect = document.getElementById('tipoDocumento');
    const numeroDocumentoInput = document.getElementById('numeroDocumento');

    if (tipoDocumentoSelect && numeroDocumentoInput) {
        // 1. Cambiar el placeholder y maxlength al seleccionar un tipo de documento
        tipoDocumentoSelect.addEventListener('change', function() {
            const tipo = this.value;
            numeroDocumentoInput.value = ''; // Limpiar el campo al cambiar de tipo

            if (tipo === 'NIT') {
                numeroDocumentoInput.placeholder = 'Ej: 900123456-7';
                numeroDocumentoInput.maxLength = 11;
            } else if (tipo === 'CC' || tipo === 'CE') {
                numeroDocumentoInput.placeholder = 'Ej: 1023456789';
                numeroDocumentoInput.maxLength = 10;
            } else {
                numeroDocumentoInput.placeholder = 'Número de Documento';
                numeroDocumentoInput.maxLength = 20; // Un valor por defecto
            }
            numeroDocumentoInput.focus(); // Poner el foco en el campo de número
        });

        // 2. Validar el número de documento cuando el usuario sale del campo
        numeroDocumentoInput.addEventListener('blur', function() {
            const tipo = tipoDocumentoSelect.value;
            const numero = this.value;

            if (!numero) return; // No validar si está vacío (el 'required' del HTML se encargará)

            let esValido = false;
            let mensajeError = '';

            if (tipo === 'NIT') {
                // Expresión regular para NIT colombiano: 9 o 10 dígitos, opcionalmente con guion y dígito de verificación.
                esValido = /^\d{9,10}(?:-\d{1})?$/.test(numero);
                mensajeError = 'El NIT no es válido. Debe contener 9 o 10 dígitos y opcionalmente un guion y dígito verificador.';
            } else if (tipo === 'CC' || tipo === 'CE') {
                // Cédulas suelen tener entre 7 y 10 dígitos numéricos.
                esValido = /^\d{7,10}$/.test(numero);
                mensajeError = 'El número de documento no es válido. Debe contener entre 7 y 10 dígitos.';
            }

            if (tipo && !esValido) { // Solo validar si se ha seleccionado un tipo
                alert(mensajeError);
                this.focus();
            }
        });
    }
});
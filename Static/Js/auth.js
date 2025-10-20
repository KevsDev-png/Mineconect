/**
 * auth.js
 * 
 * Este archivo maneja la lógica de autenticación para el modal de inicio de sesión,
 * incluyendo el cambio entre la vista de login y la de verificación de código,
 * así como la funcionalidad de los campos de entrada del código.
 * También se incluye la lógica para el menú de navegación móvil.
 */

// Se asegura de que todo el código dentro de este bloque se ejecute solo después de que
// toda la página HTML se haya cargado por completo. Es una buena práctica para evitar
// errores al intentar manipular elementos que aún no existen.
document.addEventListener('DOMContentLoaded', () => {

    /**
     * Esta función se encarga de la lógica del menú "hamburguesa" en dispositivos móviles.
     */
    function initializeMenuToggle() {
        // Busca en el HTML el botón del menú por su ID 'menu-toggle'.
        const menuToggle = document.getElementById('menu-toggle');
        // Busca en el HTML la lista de navegación por su ID 'nav-menu'.
        const navMenu = document.getElementById('nav-menu');

        // Comprueba si ambos elementos (el botón y el menú) fueron encontrados en la página.
        if (menuToggle && navMenu) {
            // Añade un "escuchador" de eventos al botón. Cuando se le haga clic...
            menuToggle.addEventListener('click', () => {
                // ...añade o quita la clase 'active' al menú. Esto se usa en el CSS
                // para mostrar u ocultar el menú.
                navMenu.classList.toggle('active');
            });
        } else {
            // Si no se encontraron los elementos, muestra un aviso en la consola del navegador.
            console.warn('Elementos del menú no encontrados.');
        }
    }

    /**
     * Esta función maneja todo el proceso de inicio de sesión: desde que el usuario
     * envía el formulario hasta que se le muestra la pantalla de verificación.
     */
    function initializeAuthFlow() {
        // Busca todos los elementos HTML necesarios para el flujo de login por sus IDs.
        const loginForm = document.getElementById('loginForm'); // El formulario de login.
        const loginView = document.getElementById('login-view'); // La sección (vista) del login.
        const verificationView = document.getElementById('verification-view'); // La sección de verificación.
        const backToLoginBtn = document.getElementById('back-to-login-btn'); // El botón para volver al login.
        const emailInput = document.getElementById('login-email'); // El campo para escribir el email.
        const emailDisplay = document.getElementById('verification-email-display'); // Donde se muestra el email ofuscado.

        // Comprueba si todos los elementos fueron encontrados. Si falta alguno, detiene la función.
        if (!loginForm || !loginView || !verificationView || !backToLoginBtn || !emailInput || !emailDisplay) {
            console.warn('No se encontraron todos los elementos para el flujo de autenticación.');
            return; // Termina la ejecución de esta función.
        }

        // Añade un "escuchador" al formulario para el evento 'submit' (cuando se intenta enviar).
        loginForm.addEventListener('submit', (event) => {
            // Previene el comportamiento por defecto del formulario, que es recargar la página.
            event.preventDefault(); 

            // Este bloque 'try...catch' intenta ofuscar el correo y maneja posibles errores.
            try {
                // Obtiene el valor (el texto) escrito en el campo del email.
                const email = emailInput.value;
                // Divide el email en dos partes usando el '@' como separador. Ej: 'usuario' y 'dominio.com'.
                const [user, domain] = email.split('@');
                // Si el correo no tiene '@', una de las partes será indefinida. Esto lanza un error.
                if (!user || !domain) {
                    throw new Error('Formato de correo inválido.');
                }
                // Crea una versión "ofuscada" del usuario: toma los primeros 4 caracteres y añade '*****'.
                const maskedUser = user.substring(0, 4) + '*****';
                // Muestra el correo ofuscado en el elemento HTML correspondiente.
                emailDisplay.textContent = `${maskedUser}@${domain}`;
            } catch (error) {
                // Si ocurre un error en el bloque 'try', se ejecuta esto.
                console.error('Error al ofuscar el correo:', error);
                // Muestra un mensaje genérico en caso de que el formato del correo sea incorrecto.
                emailDisplay.textContent = 'un correo electrónico.';
            }

            // ---
            // NOTA DE SEGURIDAD: Aquí es donde se debería llamar al (backend) para
            // verificar que el email y la contraseña son correctos y para que el servidor
            // envíe el código de verificación real.
            // ---

            // Simulación: se asume que el login fue exitoso y se cambia de vista.
            // Oculta la vista de inicio de sesión.
            loginView.style.display = 'none';
            // Muestra la vista de verificación de código.
            verificationView.style.display = 'block';
            
            // Busca el primer campo de entrada para el código de verificación.
            const firstInput = document.querySelector('.code-input');
            // Si lo encuentra, pone el cursor (foco) en él para que el usuario pueda empezar a escribir.
            if (firstInput) {
                firstInput.focus();
            }
        });

        // Añade un "escuchador" al botón de "volver atrás".
        backToLoginBtn.addEventListener('click', () => {
            // Oculta la vista de verificación.
            verificationView.style.display = 'none';
            // Muestra de nuevo la vista de inicio de sesión.
            loginView.style.display = 'block';
        });
    }

    /**
     * Esta función mejora la experiencia de usuario en los campos del código de verificación,
     * permitiendo que el cursor salte automáticamente al siguiente campo.
     */
    function initializeVerificationInputs() {
        // Selecciona TODOS los campos de entrada que tengan la clase 'code-input'.
        const codeInputs = document.querySelectorAll('.code-input');
        // Si no se encuentra ningún campo, no hace nada y termina la función.
        if (codeInputs.length === 0) return;

        // Recorre cada uno de los campos de entrada encontrados.
        codeInputs.forEach((input, index) => {
            // Añade un "escuchador" para el evento 'input' (cuando el usuario escribe algo).
            input.addEventListener('input', () => {
                // Si el campo ya tiene 1 caracter y NO es el último campo de la lista...
                if (input.value.length === 1 && index < codeInputs.length - 1) {
                    // ...mueve el foco (cursor) al siguiente campo.
                    codeInputs[index + 1].focus();
                }
            });

            // Añade un "escuchador" para el evento 'keydown' (cuando se presiona una tecla).
            input.addEventListener('keydown', (e) => {
                // Si la tecla presionada es 'Backspace' (borrar), el campo está vacío y NO es el primer campo...
                if (e.key === 'Backspace' && input.value.length === 0 && index > 0) {
                    // ...mueve el foco (cursor) al campo anterior.
                    codeInputs[index - 1].focus();
                }
            });
        });
    }

    // Finalmente, se llama a las tres funciones de inicialización para que todo empiece a funcionar.
    initializeMenuToggle();
    initializeAuthFlow();
    initializeVerificationInputs();
});

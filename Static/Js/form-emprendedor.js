document.addEventListener('DOMContentLoaded', function() {
    
    const form = document.getElementById('registro-emprendedor-form');
    const correoInput = document.getElementById('correo-emprendedor');
    const celularInput = document.getElementById('celular-emprendedor'); 

    // --- FILTRADO EN TIEMPO REAL PARA CELULAR ---
    if (celularInput) {
        celularInput.addEventListener('input', function(event) {
            this.value = this.value.replace(/[^0-9]/g, ''); // Solo permite números
        });
    }

    // --- VALIDACIÓN EN TIEMPO REAL PARA CORREO (.com) ---
    if (correoInput) {
        correoInput.addEventListener('blur', function() { 
            const correo = this.value.trim();
            if (correo.includes('@') && correo.split('@')[1].length > 0 && !correo.endsWith('.com')) {
                alert("Recuerda que el correo debe terminar en '.com'.");
            }
        });
    }
    
    // --- VALIDACIÓN FINAL AL ENVIAR EL FORMULARIO ---
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevenir el envío

            // --- 1. CAPTURAR VALORES ---
            const nombreCompleto = document.querySelector('input[name="nombre_completo"]').value.trim();
            const correo = document.getElementById('correo-emprendedor').value.trim();
            const contrasena = document.getElementById('contrasena-emprendedor').value;
            const tipoDocumento = document.querySelector('select[name="tipo_documento"]').value;
            const celular = celularInput.value; // Ya filtrado a solo números
            const programaFormacion = document.querySelector('input[name="programa_formacion"]').value.trim();
            const tituloProyecto = document.querySelector('input[name="titulo_proyecto"]').value.trim();
            const descripcionProyecto = document.querySelector('textarea[name="descripcion_proyecto"]').value.trim();
            const relacionSector = document.querySelector('input[name="relacion_sector"]').value.trim();
            const tipoApoyo = document.querySelector('input[name="tipo_apoyo"]:checked');
            const terminos = document.getElementById('terminos-emprendedor').checked;

            // --- 2. EXPRESIONES REGULARES ---
            const emailRegex = /^[^@ ]+@[^@ ]+\.[^@ ]+$/;
            // Quitamos la restricción de 8 caracteres y añadimos la complejidad
            const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*._-]).{8,}$/; 
            const numericRegex = /^[0-9]+$/; // Solo números

            // --- 3. EJECUTAR VALIDACIONES ---

            if (nombreCompleto === '') { alert("El Nombre Completo es obligatorio."); return; }
            
            // Correo
            if (!emailRegex.test(correo) || !correo.endsWith('.com')) {
                alert("El correo no es válido. Debe tener un formato correcto y terminar en '.com'.");
                return;
            }
            
            // Contraseña (Complejidad + Mínimo 8 caracteres)
            if (!passwordRegex.test(contrasena)) {
                 alert("La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial: !@#$%^&*._-");
                 return;
             }

            if (tipoDocumento === null || tipoDocumento === '') { alert("Debe seleccionar un Tipo de Documento."); return; }
            
            // Celular (Ya filtrado, solo validamos longitud)
            if (celular.length !== 10) {
                 alert("El Número de celular debe contener exactamente 10 dígitos numéricos.");
                 return;
             }

            if (programaFormacion === '') { alert("El Programa de Formación es obligatorio."); return; }
            if (tituloProyecto === '') { alert("El Título del Proyecto es obligatorio."); return; }
            if (descripcionProyecto === '') { alert("La Descripción del Proyecto es obligatoria."); return; }
            if (relacionSector === '') { alert("El campo 'Relación Con El Sector Minero' es obligatorio."); return; }
            if (!tipoApoyo) { alert("Debe seleccionar un Tipo de Apoyo."); return; }
            if (!terminos) { alert("Debe aceptar los Términos y Condiciones."); return; }

            // --- 4. SI TODO ESTÁ BIEN, ENVIAR EL FORMULARIO ---
            // Si todas las validaciones pasan, se elimina el preventDefault y se envía el formulario.
            // Ya no es necesario el alert ni llamar a form.submit() manualmente.
            event.target.submit();
        });
    }
});
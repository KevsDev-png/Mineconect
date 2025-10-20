document.addEventListener('DOMContentLoaded', function() {
    
    // --- LÓGICA DE CAMPOS CONDICIONALES ---
    const tipoContribuyenteRadios = document.querySelectorAll('input[name="tipo_contribuyente"]');
    const naturalWrapper = document.getElementById('conditional-natural-wrapper');
    const juridicaWrapper = document.getElementById('conditional-juridica-wrapper');

    if (tipoContribuyenteRadios.length > 0) {
        tipoContribuyenteRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.value === 'natural') {
                    naturalWrapper.classList.remove('hidden');
                    juridicaWrapper.classList.add('hidden');
                } else if (this.value === 'juridica') {
                    naturalWrapper.classList.add('hidden');
                    juridicaWrapper.classList.remove('hidden');
                }
            });
        });
    }

    // --- LÓGICA DE VALIDACIÓN DEL FORMULARIO ---
    const form = document.getElementById('registro-form');
    const celularInput = document.getElementById('celular'); // Selecciona input celular

    // --- FILTRADO DE ENTRADA EN TIEMPO REAL PARA CELULAR ---
    if (celularInput) {
        celularInput.addEventListener('input', function(event) {
            this.value = this.value.replace(/[^0-9]/g, ''); // Solo permite números
        });
    }
    // --- FIN FILTRADO ---

    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevenir el envío

            // --- 1. CAPTURAR VALORES ---
            const correo = document.getElementById('correo').value.trim();
            // ... (capturar otros campos necesarios para validación completa) ...
             const contrasena = document.getElementById('contrasena').value; // Sin trim
             const numDocPersonal = document.querySelector('input[name="numero_documento_personal"]').value.trim(); 
             const tipoContribuyente = document.querySelector('input[name="tipo_contribuyente"]:checked');

            // --- 2. EXPRESIONES REGULARES Y VALIDACIONES ---
            const numericRegex = /^[0-9]+$/; // Solo números
            
            // **CORREO**: Verificar formato básico Y si termina en .com
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(correo) || !correo.endsWith('.com')) { // <-- CAMBIO AQUÍ
                alert("El correo no es válido. Debe tener un formato correcto y terminar en '.com'.");
                return;
            }

            // **CONTRASEÑA**: Verificar si excede los 8 caracteres
            if (contrasena.length > 8) {
                 alert("La contraseña no puede tener más de 8 caracteres.");
                 return; 
            }
             if (contrasena.length < 1) { 
                 alert("La contraseña no puede estar vacía.");
                 return;
             }

            // **NÚMERO DE DOCUMENTO PERSONAL**: Verificar si es numérico
             if (numDocPersonal === '') {
                 alert("El Número de documento es obligatorio.");
                 return;
             }
             if (!numericRegex.test(numDocPersonal)) {
                 alert("El Número de documento solo debe contener números.");
                 return;
             }

            // **CELULAR**: Verificar si son exactamente 10 dígitos y solo números (usando el input ya filtrado)
             const celular = celularInput.value; // Ya filtrado a solo números
             if (celular.length !== 10) {
                 alert("El Número de celular debe contener exactamente 10 dígitos numéricos.");
                 return;
             }

            // **VALIDACIONES CONDICIONALES (NIT / Doc Natural)**
             if (tipoContribuyente) { 
                 if (tipoContribuyente.value === 'natural') {
                     const numDocNatural = document.getElementById('numero-documento').value.trim();
                     if (numDocNatural === '') {
                         alert("El Número de documento para Persona Natural es obligatorio.");
                         return;
                     }
                     if (!numericRegex.test(numDocNatural)) {
                         alert("El Número de documento solo debe contener números.");
                         return;
                     }
                 } else if (tipoContribuyente.value === 'juridica') {
                     const nit = document.getElementById('nit').value.trim();
                     if (nit === '') {
                         alert("El NIT es obligatorio.");
                         return;
                     }
                     if (!numericRegex.test(nit)) {
                         alert("El NIT solo debe contener números.");
                         return;
                     }
                 }
             } else {
                 alert("Debe seleccionar un Tipo de Contribuyente.");
                 return;
             }

            // --- (Añadir verificaciones para otros campos requeridos aquí si es necesario) ---
             const terminos = document.getElementById('terminos');
             if (terminos && !terminos.checked) {
                 alert("Debe aceptar los Términos y Condiciones.");
                 return;
             }

            // --- 3. ENVIAR FORMULARIO ---
            alert("¡Formulario validado con éxito!"); 
            form.submit(); 
        });
    }
});
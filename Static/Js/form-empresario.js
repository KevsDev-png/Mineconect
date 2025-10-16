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

    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevenimos el envío

            // --- 1. CAPTURAR VALORES ---
            const nombreCompleto = document.querySelector('input[name="nombre_completo"]').value.trim();
            const correo = document.getElementById('correo').value.trim();
            const contrasena = document.getElementById('contrasena').value;
            const tipoDocPersonal = document.querySelector('select[name="tipo_documento_personal"]').value;
            const numDocPersonal = document.querySelector('input[name="numero_documento_personal"]').value.trim();
            const celular = document.querySelector('input[name="numero_celular"]').value.trim();
            const nombreEmpresa = document.querySelector('input[name="nombre_empresa"]').value.trim();
            const tipoContribuyente = document.querySelector('input[name="tipo_contribuyente"]:checked');
            const tamanoEmpresa = document.querySelector('input[name="tamano"]:checked');
            const etapa = document.querySelector('input[name="etapa"]:checked');
            const sectorProd = document.querySelector('select[name="sector_produccion"]').value;
            const sectorTrans = document.querySelector('select[name="sector_transformacion"]').value;
            const sectorComer = document.querySelector('select[name="sector_comercializacion"]').value;
            const terminos = document.getElementById('terminos').checked;

            // --- 2. EXPRESIONES REGULARES PARA VALIDACIÓN ---
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*._-]).{8,}$/;
            
            // NUEVA: Regla para solo números
            const numericRegex = /^[0-9]+$/; 
            
            // Mantenemos la regla de 10 dígitos para el celular (que ya es numérica)
            const celularRegex = /^[0-9]{10}$/;

            // --- 3. EJECUTAR VALIDACIONES ---
            
            // Info Personal
            if (nombreCompleto === '') {
                alert("El Nombre Completo es obligatorio.");
                return;
            }
            if (!emailRegex.test(correo)) {
                alert("El correo no es válido, por favor ingrese un correo válido.");
                return;
            }
            if (!passwordRegex.test(contrasena)) {
                alert("La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial: !@#$%^&*._-");
                return;
            }
            if (tipoDocPersonal === null || tipoDocPersonal === '') {
                alert("Debe seleccionar un tipo de documento.");
                return;
            }
            if (numDocPersonal === '') {
                alert("El Número de documento es obligatorio.");
                return;
            }
            // NUEVA VALIDACIÓN NUMÉRICA
            if (!numericRegex.test(numDocPersonal)) {
                alert("El Número de documento solo debe contener números (sin puntos, espacios ni guiones).");
                return;
            }
            if (!celularRegex.test(celular)) {
                alert("El Número de celular no es válido. Debe tener 10 dígitos numéricos.");
                return;
            }

            // Info Empresa
            if (nombreEmpresa === '') {
                alert("El Nombre de la Empresa es obligatorio.");
                return;
            }
            if (!tipoContribuyente) {
                alert("Debe seleccionar un Tipo de Contribuyente.");
                return;
            }

            // Validaciones Condicionales
            if (tipoContribuyente.value === 'natural') {
                const numDocNatural = document.getElementById('numero-documento').value.trim();
                if (numDocNatural === '') {
                    alert("El Número de documento para Persona Natural es obligatorio.");
                    return;
                }
                // NUEVA VALIDACIÓN NUMÉRICA
                if (!numericRegex.test(numDocNatural)) {
                    alert("El Número de documento solo debe contener números (sin puntos, espacios ni guiones).");
                    return;
                }
            }

            if (tipoContribuyente.value === 'juridica') {
                const nit = document.getElementById('nit').value.trim();
                if (nit === '') {
                    alert("El NIT es obligatorio.");
                    return;
                }
                // NUEVA VALIDACIÓN NUMÉRICA
                if (!numericRegex.test(nit)) {
                    alert("El NIT solo debe contener números (sin puntos, espacios ni guiones).");
                    return;
                }
            }

            if (!tamanoEmpresa) {
                alert("Debe seleccionar un Tamaño de la Empresa.");
                return;
            }
            if (!etapa) {
                alert("Debe seleccionar una Etapa de Encadenamiento.");
                return;
            }
            if (sectorProd === null || sectorProd === '') {
                alert("Debe seleccionar una actividad de Producción.");
                return;
            }
            if (sectorTrans === null || sectorTrans === '') {
                alert("Debe seleccionar una actividad de Transformación.");
                return;
            }
            if (sectorComer === null || sectorComer === '') {
                alert("Debe seleccionar una actividad de Comercialización.");
                return;
            }
            if (!terminos) {
                alert("Debe aceptar los Términos y Condiciones.");
                return;
            }

            // --- 4. ENVIAR FORMULARIO ---
            alert("¡Formulario enviado con éxito!"); // Opcional
            form.submit();
        });
    }
});
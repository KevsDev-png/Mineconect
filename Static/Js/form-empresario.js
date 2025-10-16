document.addEventListener('DOMContentLoaded', function() {
    // Seleccionamos los elementos
    const tipoContribuyenteRadios = document.querySelectorAll('input[name="tipo_contribuyente"]');
    const naturalWrapper = document.getElementById('conditional-natural-wrapper');
    const juridicaWrapper = document.getElementById('conditional-juridica-wrapper');

    // Escuchamos los cambios en los botones
    tipoContribuyenteRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'natural') {
                // Muestra "Número de documento" y oculta "NIT"
                naturalWrapper.classList.remove('hidden');
                juridicaWrapper.classList.add('hidden');
            } else if (this.value === 'juridica') {
                // Muestra "NIT" y oculta "Número de documento"
                naturalWrapper.classList.add('hidden');
                juridicaWrapper.classList.remove('hidden');
            }
        });
    });
});
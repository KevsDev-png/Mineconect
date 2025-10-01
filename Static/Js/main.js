document.addEventListener('DOMContentLoaded', () => {

    // --- LÓGICA PARA ABRIR Y CERRAR EL MODAL ---
    const registerBtn = document.getElementById('register-btn');
    const profileModal = document.getElementById('profile-modal');
    const closeModalBtn = document.getElementById('close-modal-btn');

    // Función para abrir el modal
    function openModal(event) {
        event.preventDefault(); // Previene que el enlace '#' recargue la página
        profileModal.classList.remove('hidden');
    }

    // Función para cerrar el modal
    function closeModal() {
        profileModal.classList.add('hidden');
    }

    // Asignar eventos a los botones
    if (registerBtn && profileModal && closeModalBtn) {
        registerBtn.addEventListener('click', openModal);
        closeModalBtn.addEventListener('click', closeModal);

        // Opcional: Cerrar el modal si se hace clic en el fondo oscuro
        profileModal.addEventListener('click', (event) => {
            // Se asegura de que el clic fue en el fondo (overlay) y no en el contenido
            if (event.target === profileModal) {
                closeModal();
            }
        });
    }


    // --- LÓGICA PARA SELECCIONAR PERFIL ---
    const profileCards = document.querySelectorAll('.profile-card');

    profileCards.forEach(card => {
        card.addEventListener('click', () => {
            // 1. Quitar la clase 'selected' de TODAS las tarjetas
            profileCards.forEach(c => c.classList.remove('selected'));
            // 2. Añadir la clase 'selected' solo a la tarjeta clickeada
            card.classList.add('selected');
        });
    });

});
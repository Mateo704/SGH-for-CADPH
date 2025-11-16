(function() {
  document.addEventListener('DOMContentLoaded', function() {
    const userSelect = document.getElementById('id_user');
    const nombresInput = document.getElementById('id_nombres');
    const docInput = document.getElementById('id_numero_documento');

    if (!userSelect || !nombresInput || !docInput) return;

    function actualizarDatos() {
      const option = userSelect.options[userSelect.selectedIndex];
      if (!option || !option.value) {
        nombresInput.value = '';
        docInput.value = '';
        return;
      }

      const text = option.text; // Ej: "1234567890 - pepito"

      const parts = text.split(' - ');
      const numero = (parts[0] || '').trim();
      const nombre = (parts[1] || '').trim();

      docInput.value = numero;
      nombresInput.value = nombre;
    }

    // Cuando cambie el usuario seleccionado
    userSelect.addEventListener('change', actualizarDatos);

    // También al cargar la página, por si ya viene uno seleccionado
    actualizarDatos();
  });
})();

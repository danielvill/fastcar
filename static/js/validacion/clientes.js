// Validacion si los campos estan vacios
document.querySelector('form').onsubmit = function (e) {
    var inputs = this.querySelectorAll('input');
    var todosLlenos = true; // Asume que todos los campos están llenos

    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].value === '') {
            todosLlenos = false; // Si un campo está vacío, establece todosLlenos en falso
            break; // No necesitas verificar el resto de los campos, así que puedes salir del bucle
        }
    }

    if (!todosLlenos) {
        e.preventDefault(); // Previene el envío del formulario
        alert('Los campos estan vacios');
    } else {
        alert('Guardado exitosamente');
    }
};

// Validacion de numero telefonico
document.querySelector('form').addEventListener('submit', function(event) {
    var telefono = document.querySelector('input[name="telefono"]').value;
    var regex = /^09\d{8}$/; // Expresión regular para validar números de celular ecuatorianos

    if (!regex.test(telefono)) {
        alert('Por favor, ingresa un número de celular ecuatoriano válido.');
        event.preventDefault(); // Evita que el formulario se envíe
    }
});

// Validación de campos vacíos
document.querySelector('form').onsubmit = function (e) {
    var inputs = this.querySelectorAll('input');
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].value === '') {
            e.preventDefault();
            alert('Los campos estan vacion');
            return;
        }
        else {
            alert('Guardado exitosamente');
            return;
        }

    }
}

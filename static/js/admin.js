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
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Los campos estan vacios'
        });
    } 
};

// Validadr lo que es la cedula no tiene para ver si esta en el gobierno
function validarCedula(cedula) {
    // Verifica que tenga 10 caracteres y sea solo números
    if (cedula.length === 10 && Number.isInteger(+cedula)) {
        var digitos = cedula.split('').map(Number);
        var ultimoDigito = digitos.pop();
        var suma = digitos.reduce(function (acc, curr, i) {
            var valor = (i % 2 === 0) ? curr * 2 : curr;
            valor = (valor > 9) ? valor - 9 : valor;
            return acc + valor;
        }, 0);
        var digitoVerificador = 10 - (suma % 10);
        digitoVerificador = (digitoVerificador === 10) ? 0 : digitoVerificador;
        return ultimoDigito === digitoVerificador;
    } else {
        return false;
    }
}

document.querySelector('form').addEventListener('submit', function (e) {
    var cedula = document.querySelector('input[name="cedula"]').value;
    if (!validarCedula(cedula)) {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'La cedula no es valida'
        });
        e.preventDefault(); // Previene el envío del formulario
    }
});


// Validar Correo
function validarcorreo() {
    let correo = document.getElementById('correo').value;
    let regex = /^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$/;
    if (!regex.test(correo)) {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Ingresa un correo valido'
        });
        return false;
    }
}


function limitarEntrada() {
    let x = document.getElementById("miInput");
    if (x.value.length > 10) {
        x.value = x.value.slice(0, 10);
    }
}
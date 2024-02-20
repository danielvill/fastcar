//  Este es oara preguntar de la edicion y eliminacion
$(document).ready(function () {
    $(".editar").click(function (event) {
        if (!confirm("¿Estás seguro de que quieres editar?")) {
            event.preventDefault();
        }
    });

    $(".eliminar").click(function (event) {
        if (!confirm("¿Estás seguro de que quieres eliminar?")) {
            event.preventDefault();
        }
    });
});
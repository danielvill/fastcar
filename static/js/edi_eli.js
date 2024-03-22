$(".eliminar").click(function (event) {
    event.preventDefault();
    var url = $(this).attr('href'); // Guarda la URL del enlace
    Swal.fire({
        title: '¿Estás seguro?',
        text: "¿Estás seguro de que quieres eliminar?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, eliminar!',
        cancelButtonText: 'No, cancelar!'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = url; // Navega a la URL del enlace
        }
    });
});
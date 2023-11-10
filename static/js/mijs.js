function deleteUser(rut) {
  if (confirm('¿Estás seguro de que quieres eliminar este usuario?')) {
    fetch('/delete_user/' + rut, {
      method: 'DELETE',
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === 'success') {
          // Recarga la página
          location.reload();
        } else {
          // Muestra un mensaje de error
          alert(data.message);
        }
      });
  }
}

function deleteProduct(idarticulo) {
  if (confirm('¿Estás seguro de que quieres eliminar este producto?')) {
    fetch('/delete_product/' + idarticulo, {
      method: 'DELETE',
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === 'success') {
          // Recarga la página
          location.reload();
        } else {
          // Muestra un mensaje de error
          alert(data.message);
        }
      });
  }
}

let indice = 0;

function moverCarrusel(direccion) {
    const track = document.getElementById("carousel-track");
    const items = document.querySelectorAll(".carousel-item");
    const ancho = items[0].offsetWidth;
    indice += direccion;

    if (indice < 0) indice = items.length - 1;
    if (indice >= items.length) indice = 0;

    track.style.transform = `translateX(${-indice * ancho}px)`;
}

function filtrarCategoria(cat) {
    document.querySelectorAll(".card").forEach(card => {
        if (cat === "Todos" || card.dataset.categoria === cat) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }
    });
}

function verPassword() {
    let input = document.getElementById("password");
    input.type = input.type === "password" ? "text" : "password";
}

function verificarUsuario(nombre, precio){

    let usuario = document.body.getAttribute("data-usuario");

    if(!usuario || usuario === ""){
        document.getElementById("popupLogin").style.display = "flex";
        return;
    }

    agregarCarrito(nombre, precio);
}

function cerrarPopup(){
    document.getElementById("popupLogin").style.display = "none";
}

function agregarCarrito(nombre, precio){
    alert("Producto agregado al carrito: " + nombre);
}
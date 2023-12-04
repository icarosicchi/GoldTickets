document.addEventListener('DOMContentLoaded', function () {
  const menuBtn = document.getElementById('menu-btn');
  const navegacaoPrincipal = document.getElementById('navegacao-principal');
  const menuResponsivo = document.getElementById('menu-responsivo');

  menuBtn.addEventListener('click', function () {
    navegacaoPrincipal.classList.toggle('active');
    menuResponsivo.classList.toggle('active');
  });
});

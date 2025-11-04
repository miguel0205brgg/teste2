// Sistema de Abas
document.addEventListener('DOMContentLoaded', function() {
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabPanes = document.querySelectorAll('.tab-pane');

  // Funcionalidade de Abas
  tabBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      const tabName = this.getAttribute('data-tab');
      
      // Remover classe active de todos os botões e panes
      tabBtns.forEach(b => b.classList.remove('active'));
      tabPanes.forEach(pane => pane.classList.remove('active'));
      
      // Adicionar classe active ao botão clicado e seu pane correspondente
      this.classList.add('active');
      document.getElementById(tabName).classList.add('active');
    });
  });

  // Botões de Ação
  const editarBtn = document.getElementById('editarBtn');
  const editarEnderecoBtn = document.getElementById('editarEnderecoBtn');
  const alterarSenhaBtn = document.getElementById('alterarSenhaBtn');
  const sairBtn = document.getElementById('sairBtn');

  if (editarBtn) {
    editarBtn.addEventListener('click', function() {
      alert('Funcionalidade de edição de perfil em desenvolvimento');
      // Aqui você pode redirecionar para uma página de edição ou abrir um modal
    });
  }

  if (editarEnderecoBtn) {
    editarEnderecoBtn.addEventListener('click', function() {
      alert('Funcionalidade de edição de endereço em desenvolvimento');
      // Aqui você pode redirecionar para uma página de edição ou abrir um modal
    });
  }

  if (alterarSenhaBtn) {
    alterarSenhaBtn.addEventListener('click', function() {
      alert('Funcionalidade de alteração de senha em desenvolvimento');
      // Aqui você pode redirecionar para uma página de alteração de senha ou abrir um modal
    });
  }

  if (sairBtn) {
    sairBtn.addEventListener('click', function() {
      if (confirm('Tem certeza que deseja sair?')) {
        window.location.href = '/logout';
      }
    });
  }

  // Animação de entrada
  const perfilCard = document.querySelector('.perfil-card');
  if (perfilCard) {
    perfilCard.style.animation = 'slideIn 0.5s ease';
  }
});

// Animação de slide in
const style = document.createElement('style');
style.textContent = `
  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
`;
document.head.appendChild(style);

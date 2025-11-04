// Sistema de Abas e Edição de Perfil
document.addEventListener('DOMContentLoaded', function() {
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabPanes = document.querySelectorAll('.tab-pane');
  const modal = document.getElementById('modalEditarPerfil');
  const editarBtn = document.getElementById('editarBtn');
  const fecharModalBtn = document.getElementById('fecharModalBtn');
  const cancelarBtn = document.getElementById('cancelarBtn');
  const formEditarPerfil = document.getElementById('formEditarPerfil');
  const editarEnderecoBtn = document.getElementById('editarEnderecoBtn');
  const alterarSenhaBtn = document.getElementById('alterarSenhaBtn');
  const sairBtn = document.getElementById('sairBtn');

  // ===== Funcionalidade de Abas =====
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

  // ===== Funcionalidade de Modal de Edição de Perfil =====
  
  // Abrir modal
  if (editarBtn) {
    editarBtn.addEventListener('click', function() {
      modal.classList.add('active');
      document.body.style.overflow = 'hidden'; // Previne scroll da página
    });
  }

  // Fechar modal ao clicar no botão X
  if (fecharModalBtn) {
    fecharModalBtn.addEventListener('click', function() {
      fecharModal();
    });
  }

  // Fechar modal ao clicar em Cancelar
  if (cancelarBtn) {
    cancelarBtn.addEventListener('click', function() {
      fecharModal();
    });
  }

  // Fechar modal ao clicar fora do conteúdo
  window.addEventListener('click', function(event) {
    if (event.target === modal) {
      fecharModal();
    }
  });

  // Função para fechar o modal
  function fecharModal() {
    modal.classList.remove('active');
    document.body.style.overflow = 'auto'; // Restaura scroll da página
  }

  // Submeter formulário de edição
  if (formEditarPerfil) {
    formEditarPerfil.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const nome = document.getElementById('nomeInput').value;
      const email = document.getElementById('emailInput').value;

      // Validação básica
      if (!nome.trim() || !email.trim()) {
        alert('Por favor, preencha todos os campos');
        return;
      }

      // Enviar dados para o servidor
      fetch('/api/perfil/atualizar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          nome: nome,
          email: email
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          alert('Perfil atualizado com sucesso!');
          fecharModal();
          // Recarregar a página para mostrar as alterações
          location.reload();
        } else {
          alert('Erro ao atualizar perfil: ' + (data.message || 'Erro desconhecido'));
        }
      })
      .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao atualizar perfil. Tente novamente.');
      });
    });
  }

  // ===== Botões de Ação =====

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

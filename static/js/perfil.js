// Sistema de Abas e Edição de Perfil
document.addEventListener('DOMContentLoaded', function() {
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabPanes = document.querySelectorAll('.tab-pane');
  
  // ===== Modais =====
  const modalEditarPerfil = document.getElementById('modalEditarPerfil');
  const modalEditarEndereco = document.getElementById('modalEditarEndereco');
  const modalAlterarSenha = document.getElementById('modalAlterarSenha');
  
  // ===== Botões de Edição =====
  const editarBtn = document.getElementById('editarBtn');
  const editarEnderecoBtn = document.getElementById('editarEnderecoBtn');
  const alterarSenhaBtn = document.getElementById('alterarSenhaBtn');
  const sairBtn = document.getElementById('sairBtn');
  
  // ===== Botões de Fechar Modal =====
  const fecharModalBtn = document.getElementById('fecharModalBtn');
  const fecharModalEnderecoBtn = document.getElementById('fecharModalEnderecoBtn');
  const fecharModalSenhaBtn = document.getElementById('fecharModalSenhaBtn');
  
  // ===== Botões de Cancelar =====
  const cancelarBtn = document.getElementById('cancelarBtn');
  const cancelarEnderecoBtn = document.getElementById('cancelarEnderecoBtn');
  const cancelarSenhaBtn = document.getElementById('cancelarSenhaBtn');
  
  // ===== Formulários =====
  const formEditarPerfil = document.getElementById('formEditarPerfil');
  const formEditarEndereco = document.getElementById('formEditarEndereco');
  const formAlterarSenha = document.getElementById('formAlterarSenha');

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

  // ===== Funções Auxiliares =====
  
  function fecharModal(modal) {
    modal.classList.remove('active');
    document.body.style.overflow = 'auto';
  }

  function abrirModal(modal) {
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function mostrarMensagem(mensagem, tipo = 'sucesso') {
    const alertClass = tipo === 'sucesso' ? 'alert-sucesso' : 'alert-erro';
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert ${alertClass}`;
    alertDiv.innerHTML = `
      <i class="fas fa-${tipo === 'sucesso' ? 'check-circle' : 'exclamation-circle'}"></i>
      <span>${mensagem}</span>
    `;
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
      alertDiv.remove();
    }, 4000);
  }

  // ===== Modal de Edição de Perfil =====
  
  if (editarBtn) {
    editarBtn.addEventListener('click', function() {
      abrirModal(modalEditarPerfil);
    });
  }

  if (fecharModalBtn) {
    fecharModalBtn.addEventListener('click', function() {
      fecharModal(modalEditarPerfil);
    });
  }

  if (cancelarBtn) {
    cancelarBtn.addEventListener('click', function() {
      fecharModal(modalEditarPerfil);
    });
  }

  if (formEditarPerfil) {
    formEditarPerfil.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const nome = document.getElementById('nomeInput').value;
      const email = document.getElementById('emailInput').value;

      if (!nome.trim() || !email.trim()) {
        mostrarMensagem('Por favor, preencha todos os campos', 'erro');
        return;
      }

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
          mostrarMensagem('Perfil atualizado com sucesso!');
          fecharModal(modalEditarPerfil);
          setTimeout(() => {
            location.reload();
          }, 1500);
        } else {
          mostrarMensagem('Erro ao atualizar perfil: ' + (data.message || 'Erro desconhecido'), 'erro');
        }
      })
      .catch(error => {
        console.error('Erro:', error);
        mostrarMensagem('Erro ao atualizar perfil. Tente novamente.', 'erro');
      });
    });
  }

  // ===== Modal de Edição de Endereço =====
  
  if (editarEnderecoBtn) {
    editarEnderecoBtn.addEventListener('click', function() {
      abrirModal(modalEditarEndereco);
    });
  }

  if (fecharModalEnderecoBtn) {
    fecharModalEnderecoBtn.addEventListener('click', function() {
      fecharModal(modalEditarEndereco);
    });
  }

  if (cancelarEnderecoBtn) {
    cancelarEnderecoBtn.addEventListener('click', function() {
      fecharModal(modalEditarEndereco);
    });
  }

  if (formEditarEndereco) {
    formEditarEndereco.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const rua = document.getElementById('ruaInput').value;
      const cep = document.getElementById('cepInput').value;
      const numero = document.getElementById('numeroInput').value;
      const complemento = document.getElementById('complementoInput').value;
      const telefone = document.getElementById('telefoneInput').value;

      if (!rua.trim() || !cep.trim() || !numero.trim() || !telefone.trim()) {
        mostrarMensagem('Por favor, preencha todos os campos obrigatórios', 'erro');
        return;
      }

      fetch('/api/perfil/atualizar-endereco', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          rua: rua,
          cep: cep,
          numero: numero,
          complemento: complemento,
          telefone: telefone
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          mostrarMensagem('Endereço atualizado com sucesso!');
          fecharModal(modalEditarEndereco);
          setTimeout(() => {
            location.reload();
          }, 1500);
        } else {
          mostrarMensagem('Erro ao atualizar endereço: ' + (data.message || 'Erro desconhecido'), 'erro');
        }
      })
      .catch(error => {
        console.error('Erro:', error);
        mostrarMensagem('Erro ao atualizar endereço. Tente novamente.', 'erro');
      });
    });
  }

  // ===== Modal de Alteração de Senha =====
  
  if (alterarSenhaBtn) {
    alterarSenhaBtn.addEventListener('click', function() {
      abrirModal(modalAlterarSenha);
    });
  }

  if (fecharModalSenhaBtn) {
    fecharModalSenhaBtn.addEventListener('click', function() {
      fecharModal(modalAlterarSenha);
    });
  }

  if (cancelarSenhaBtn) {
    cancelarSenhaBtn.addEventListener('click', function() {
      fecharModal(modalAlterarSenha);
    });
  }

  if (formAlterarSenha) {
    formAlterarSenha.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const senhaAtual = document.getElementById('senhaAtualInput').value;
      const novaSenha = document.getElementById('novaSenhaInput').value;
      const confirmarSenha = document.getElementById('confirmarSenhaInput').value;

      if (!senhaAtual.trim() || !novaSenha.trim() || !confirmarSenha.trim()) {
        mostrarMensagem('Por favor, preencha todos os campos', 'erro');
        return;
      }

      if (novaSenha !== confirmarSenha) {
        mostrarMensagem('As senhas não coincidem', 'erro');
        return;
      }

      if (novaSenha.length < 6) {
        mostrarMensagem('A nova senha deve ter no mínimo 6 caracteres', 'erro');
        return;
      }

      fetch('/api/perfil/alterar-senha', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          senha_atual: senhaAtual,
          nova_senha: novaSenha
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          mostrarMensagem('Senha alterada com sucesso!');
          fecharModal(modalAlterarSenha);
          formAlterarSenha.reset();
          setTimeout(() => {
            location.reload();
          }, 1500);
        } else {
          mostrarMensagem('Erro ao alterar senha: ' + (data.message || 'Erro desconhecido'), 'erro');
        }
      })
      .catch(error => {
        console.error('Erro:', error);
        mostrarMensagem('Erro ao alterar senha. Tente novamente.', 'erro');
      });
    });
  }

  // ===== Botões de Ação =====

  if (sairBtn) {
    sairBtn.addEventListener('click', function() {
      if (confirm('Tem certeza que deseja sair?')) {
        window.location.href = '/logout';
      }
    });
  }

  // ===== Fechar Modal ao Clicar Fora =====
  window.addEventListener('click', function(event) {
    if (event.target === modalEditarPerfil) {
      fecharModal(modalEditarPerfil);
    }
    if (event.target === modalEditarEndereco) {
      fecharModal(modalEditarEndereco);
    }
    if (event.target === modalAlterarSenha) {
      fecharModal(modalAlterarSenha);
    }
  });

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

  .alert {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 15px 20px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 10px;
    z-index: 3000;
    animation: slideIn 0.3s ease;
    font-weight: 600;
  }

  .alert-sucesso {
    background-color: #51CF66;
    color: #fff;
  }

  .alert-erro {
    background-color: #FF6B6B;
    color: #fff;
  }
`;
document.head.appendChild(style);

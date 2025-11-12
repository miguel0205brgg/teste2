document.addEventListener('DOMContentLoaded', function() {
  const togglePassword = document.getElementById('togglePassword');
  const passwordInput = document.getElementById('password');

  // Mostrar/ocultar senha
  if (togglePassword && passwordInput) {
    togglePassword.addEventListener('click', function() {
      const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
      passwordInput.setAttribute('type', type);
      const icon = this.querySelector('i');
      if (type === 'password') {
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
      } else {
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
      }
    });
  }

  // Validação e envio do formulário de login normal
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const email = document.getElementById('email').value.trim();
      const senha = document.getElementById('password').value;

      if (!email || !senha) {
        alert('Por favor, preencha todos os campos.');
        return;
      }

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        alert('Por favor, insira um e-mail válido.');
        return;
      }

      fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, senha }),
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          window.location.href = data.redirect_url;
        } else {
          alert(data.message || "Erro ao fazer login. Tente novamente.");
        }
      })
      .catch(error => {
        console.error("Erro:", error);
        alert("Erro de conexão. Tente novamente mais tarde.");
      });
    });
  }

  // Foco animado nos inputs
  const inputs = document.querySelectorAll('.form-group input');
  inputs.forEach(input => {
    input.addEventListener('focus', function() {
      this.parentElement.classList.add('focused');
    });
    input.addEventListener('blur', function() {
      if (!this.value) this.parentElement.classList.remove('focused');
    });
  });

  // Botão de login com Google
  const googleBtn = document.getElementById('googleLogin');
  if (googleBtn) {
    googleBtn.addEventListener('click', async function(e) {
      e.preventDefault();

      try {
        const response = await fetch("/api/set_token", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ access_token: "TOKEN_DE_EXEMPLO" }) // substituir pelo token real
        });
        const data = await response.json();

        if (data.usuario_id) {
          window.location.href = data.redirect_url;
        } else {
          alert(data.error || "Erro ao entrar com Google.");
        }
      } catch (err) {
        console.error(err);
        alert("Erro ao processar login com Google.");
      }
    });
  }

  // Botão de login com Facebook (temporário)
  const facebookBtn = document.querySelector('.btn-facebook');
  if (facebookBtn) {
    facebookBtn.addEventListener('click', function(e) {
      e.preventDefault();
      alert('Funcionalidade de login com Facebook será implementada em breve!');
    });
  }
});

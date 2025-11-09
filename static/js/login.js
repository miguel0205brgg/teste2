// Funcionalidade de mostrar/ocultar senha
document.addEventListener('DOMContentLoaded', function() {
  const togglePassword = document.getElementById('togglePassword');
  const passwordInput = document.getElementById('password');

  if (togglePassword && passwordInput) {
    togglePassword.addEventListener('click', function() {
      // Alternar o tipo do input entre 'password' e 'text'
      const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
      passwordInput.setAttribute('type', type);
      
      // Alternar o ícone do olho
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

  // Validação do formulário
  const loginForm = document.getElementById('loginForm');
  
  if (loginForm) {
    loginForm.addEventListener('submit', function(e) {
      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value;

      // Validação básica
      if (!email || !password) {
        e.preventDefault();
        alert('Por favor, preencha todos os campos.');
        return false;
      }

      // Validação de email
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        e.preventDefault();
        alert('Por favor, insira um e-mail válido.');
        return false;
      }

      // Se chegou até aqui, o formulário pode ser enviado
      // return true;
      e.preventDefault(); // Previne o envio padrão do formulário

      fetch("/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email: email, senha: password }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            window.location.href = data.redirect_url; // Redireciona para a URL fornecida pelo backend
          } else {
            alert(data.message || "Erro ao fazer login. Tente novamente.");
          }
        })
        .catch((error) => {
          console.error("Erro:", error);
          alert("Erro de conexão. Tente novamente mais tarde.");
        });
    });
  }

  // Animação de foco nos inputs
  const inputs = document.querySelectorAll('.form-group input');
  inputs.forEach(input => {
    input.addEventListener('focus', function() {
      this.parentElement.classList.add('focused');
    });

    input.addEventListener('blur', function() {
      if (!this.value) {
        this.parentElement.classList.remove('focused');
      }
    });
  });

  // Botões de login social (funcionalidade real implementada)
  // const googleBtn = document.querySelector('.btn-google');
  const facebookBtn = document.querySelector('.btn-facebook');

  // if (googleBtn) {
  //   googleBtn.addEventListener('click', function(e) {
  //     e.preventDefault();
  //     alert('Funcionalidade de login com Google será implementada em breve!');
  //   });
  // }

  if (facebookBtn) {
    facebookBtn.addEventListener('click', function(e) {
      e.preventDefault();
      alert('Funcionalidade de login com Facebook será implementada em breve!');
    });
  }
});


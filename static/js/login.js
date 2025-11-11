document.addEventListener('DOMContentLoaded', function() {
  const togglePassword = document.getElementById('togglePassword');
  const passwordInput = document.getElementById('password');
  const loginForm = document.getElementById('loginForm');
  const googleBtn = document.getElementById('googleLogin');

  // Mostrar/ocultar senha
  if (togglePassword && passwordInput) {
    togglePassword.addEventListener('click', function() {
      const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
      passwordInput.setAttribute('type', type);
      const icon = this.querySelector('i');
      icon.classList.toggle('fa-eye');
      icon.classList.toggle('fa-eye-slash');
    });
  }

  // Login normal
  if (loginForm) {
    loginForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const email = document.getElementById('email').value.trim();
      const senha = document.getElementById('password').value.trim();

      if (!email || !senha) {
        alert('Preencha todos os campos.');
        return;
      }

      fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, senha })
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) window.location.href = data.redirect_url;
        else alert(data.message || 'Erro ao fazer login.');
      })
      .catch(() => alert('Erro de conexão.'));
    });
  }

  // Login com Google
  if (googleBtn) {
    googleBtn.addEventListener('click', function(e) {
      e.preventDefault();
      window.location.href = '/api/login/google';
    });
  }
});

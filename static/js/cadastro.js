document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("cadastroForm");
  const senhaInput = document.getElementById("senha");
  const confirmarSenhaInput = document.getElementById("confirmar_senha");
  const senhaFeedback = document.getElementById("senha-feedback");
  const togglePasswordIcons = document.querySelectorAll(".toggle-password");
  const cepInput = document.getElementById("cep");
  const ruaInput = document.getElementById("rua");
  const telefoneInput = document.getElementById("telefone");

  // Mostrar/Esconder senha
  togglePasswordIcons.forEach(icon => {
    icon.addEventListener("click", function() {
      const input = this.previousElementSibling;
      const type = input.getAttribute("type") === "password" ? "text" : "password";
      input.setAttribute("type", type);
      this.classList.toggle("fa-eye");
      this.classList.toggle("fa-eye-slash");
    });
  });

  // Validação da força da senha
  function validarForcaSenha(senha) {
    if (senha.length < 8) {
      senhaFeedback.textContent = "A senha deve ter no mínimo 8 caracteres.";
      senhaFeedback.className = "feedback-error";
      return false;
    }
    const temMaiuscula = /[A-Z]/.test(senha);
    const temMinuscula = /[a-z]/.test(senha);
    const temNumero = /[0-9]/.test(senha);
    const temEspecial = /[!@#$%^&*(),.?":{}|<>]/.test(senha);
    const forcas = [temMaiuscula, temMinuscula, temNumero, temEspecial].filter(Boolean).length;

    if (forcas < 3) {
      senhaFeedback.textContent = "A senha deve conter pelo menos 3 dos seguintes: maiúsculas, minúsculas, números, caracteres especiais.";
      senhaFeedback.className = "feedback-error";
      return false;
    }

    if (forcas === 3) {
      senhaFeedback.textContent = "Senha média. Considere adicionar mais caracteres.";
      senhaFeedback.className = "feedback-warning";
      return true;
    }

    senhaFeedback.textContent = "Senha forte!";
    senhaFeedback.className = "feedback-success";
    return true;
  }

  // Conferir se senhas coincidem
  function validarSenhas() {
    if (senhaInput.value !== confirmarSenhaInput.value) {
      senhaFeedback.textContent = "As senhas não coincidem.";
      confirmarSenhaInput.setCustomValidity("As senhas não coincidem.");
      return false;
    } else {
      confirmarSenhaInput.setCustomValidity("");
      validarForcaSenha(senhaInput.value);
      return true;
    }
  }

  senhaInput.addEventListener("input", () => { validarForcaSenha(senhaInput.value); validarSenhas(); });
  confirmarSenhaInput.addEventListener("input", validarSenhas);

  // Máscara de CEP
  if (cepInput) {
    cepInput.addEventListener("input", (e) => {
      let value = e.target.value.replace(/\D/g, "");
      value = value.replace(/^(\d{5})(\d)/, "$1-$2");
      e.target.value = value;
      if (value.length === 9) buscarCep(value);
    });
  }

  async function buscarCep(cep) {
    try {
      const res = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
      const data = await res.json();
      if (!data.erro && ruaInput) ruaInput.value = data.logradouro;
    } catch (err) {
      console.error(err);
    }
  }

  // Máscara de telefone
  if (telefoneInput) {
    telefoneInput.addEventListener("input", (e) => {
      let v = e.target.value.replace(/\D/g, "");
      if (v.length <= 10) v = v.replace(/^(\d{2})(\d{4})(\d{0,4})/, "($1) $2-$3");
      else v = v.replace(/^(\d{2})(\d{5})(\d{0,4})/, "($1) $2-$3");
      e.target.value = v;
    });
  }

  // Envio do formulário via fetch
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (!validarSenhas() || !validarForcaSenha(senhaInput.value)) {
      alert("Corrija os erros de senha antes de continuar.");
      return;
    }

    const formData = new FormData(form);
    formData.delete("confirmar_senha"); // não enviar confirmar senha
    const data = Object.fromEntries(formData.entries());

    try {
      const res = await fetch("/api/cadastro", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
      const result = await res.json();
      if (res.ok) {
        alert("✅ Conta criada com sucesso!");
        window.location.href = result.redirect_url || "/login";
      } else {
        alert(`⚠️ ${result.message || "Erro ao cadastrar."}`);
      }
    } catch (err) {
      console.error(err);
      alert("❌ Erro de conexão com o servidor.");
    }
  });
});

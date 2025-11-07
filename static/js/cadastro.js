document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("cadastroForm");
  const cepInput = document.getElementById("cep");
  const ruaInput = document.getElementById("rua");
  const senhaInput = document.getElementById("senha");
  const confirmarSenhaInput = document.getElementById("confirmar_senha");
  const senhaFeedback = document.getElementById("senha-feedback");
  const togglePasswordIcons = document.querySelectorAll(".toggle-password");

  // 1. Funcionalidade de Mostrar/Esconder Senha
  togglePasswordIcons.forEach(icon => {
    icon.addEventListener("click", function() {
      const input = this.previousElementSibling;
      const type = input.getAttribute("type") === "password" ? "text" : "password";
      input.setAttribute("type", type);
      this.classList.toggle("fa-eye");
      this.classList.toggle("fa-eye-slash");
    });
  });

  // 2. Validação de Senha em Tempo Real e Força
  function validarForcaSenha(senha) {
    const feedback = document.getElementById("senha-feedback");
    
    if (senha.length < 8) {
        feedback.textContent = "A senha deve ter no mínimo 8 caracteres.";
        feedback.className = "feedback-error";
        return false;
    }
    
    const temMaiuscula = /[A-Z]/.test(senha);
    const temMinuscula = /[a-z]/.test(senha);
    const temNumero = /[0-9]/.test(senha);
    const temEspecial = /[!@#$%^&*(),.?":{}|<>]/.test(senha);
    
    const forcas = [temMaiuscula, temMinuscula, temNumero, temEspecial].filter(Boolean).length;
    
    if (forcas < 3) {
        feedback.textContent = "A senha deve conter pelo menos 3 dos seguintes: maiúsculas, minúsculas, números, caracteres especiais.";
        feedback.className = "feedback-error";
        return false;
    }
    
    if (forcas === 3) {
        feedback.textContent = "Senha média. Considere adicionar mais caracteres.";
        feedback.className = "feedback-warning";
        return true;
    }
    
    feedback.textContent = "Senha forte!";
    feedback.className = "feedback-success";
    return true;
  }

  function validarSenhas() {
    if (senhaInput.value && confirmarSenhaInput.value) {
      if (senhaInput.value !== confirmarSenhaInput.value) {
        senhaFeedback.textContent = "As senhas não coincidem.";
        confirmarSenhaInput.setCustomValidity("As senhas não coincidem.");
        return false;
      } else {
        senhaFeedback.textContent = "";
        confirmarSenhaInput.setCustomValidity("");
        return true;
      }
    }
    return false;
  }

  senhaInput.addEventListener("input", function() {
    validarForcaSenha(this.value);
    validarSenhas();
  });
  confirmarSenhaInput.addEventListener("input", validarSenhas);

  // 4. Submissão do Formulário - Ajustar validação de senha
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      
      if (!validarSenhas() || !validarForcaSenha(senhaInput.value)) {
        alert("Por favor, corrija os erros de senha antes de continuar.");
        return;
      }
      
      // ... restante do código de submissão
    });
  }


  // 3. Máscara e Autopreenchimento de CEP
  if (cepInput) {
    cepInput.addEventListener("input", (e) => {
      let value = e.target.value.replace(/\D/g, ""); // Remove tudo que não é dígito
      value = value.replace(/^(\d{5})(\d)/, "$1-$2"); // Adiciona o hífen
      e.target.value = value;

      if (value.length === 9) { // CEP completo
        buscarCep(value);
      }
    });
  }

  // Máscara de telefone (Correção 4)
  const telefoneInput = document.getElementById("telefone");
  if (telefoneInput) {
    telefoneInput.addEventListener("input", (e) => {
      let value = e.target.value.replace(/\D/g, ""); // Remove tudo que não é dígito
      
      if (value.length <= 10) {
          // Formato: (XX) XXXX-XXXX
          value = value.replace(/^(\d{2})(\d{4})(\d{0,4}).*/, "($1) $2-$3");
      } else {
          // Formato: (XX) XXXXX-XXXX
          value = value.replace(/^(\d{2})(\d{5})(\d{0,4}).*/, "($1) $2-$3");
      }
      
      e.target.value = value;
    });
  }

  async function buscarCep(cep) {
    try {
      const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
      const data = await response.json();

      if (!data.erro) {
        if (ruaInput) {
          ruaInput.value = data.logradouro;
          ruaInput.style.backgroundColor = "#e8f5e9"; // Indicação visual de preenchimento automático
        }
        const numeroInput = document.getElementById("numero");
        if (numeroInput) numeroInput.focus(); // Move o foco para o número
      } else {
        alert("CEP não encontrado. Por favor, preencha o endereço manualmente.");
        if (ruaInput) {
          ruaInput.value = "";
          ruaInput.focus();
        }
      }
    } catch (error) {
      console.error("Erro ao buscar CEP:", error);
      alert("Erro ao buscar CEP. Verifique sua conexão e tente novamente, ou preencha o endereço manualmente.");
      if (ruaInput) {
        ruaInput.focus();
      }
    }
  }

  // 4. Submissão do Formulário
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      
      // A validação de senhas já é feita na função validarSenhas e validarForcaSenha
      // Apenas garantir que a validação do formulário passou
      if (!form.checkValidity()) {
        alert("Por favor, preencha todos os campos obrigatórios corretamente.");
        return;
      }

      // Validar campos de endereço obrigatórios
      const cep = document.getElementById("cep").value.trim();
      const rua = document.getElementById("rua").value.trim();
      const numero = document.getElementById("numero").value.trim();
      const telefone = document.getElementById("telefone").value.trim();

      if (!cep || !rua || !numero || !telefone) {
        alert("Por favor, preencha todos os campos obrigatórios do endereço (CEP, Rua, Número e Telefone).");
        return;
      }

      // Lógica de carregamento
      const submitBtn = form.querySelector(".btn-cadastro-submit");
      const btnText = submitBtn.querySelector(".btn-text");
      const btnLoader = submitBtn.querySelector(".btn-loader");
      if (btnText) btnText.style.display = "none";
      if (btnLoader) btnLoader.style.display = "block";
      submitBtn.disabled = true;

      // Remover o campo confirmar_senha do envio (Correção 5)
      const formData = new FormData(form);
      formData.delete('confirmar_senha');
      const data = Object.fromEntries(formData.entries());



      // Adicionar campos de endereço ao objeto de dados
      data.cep = cep;
      data.rua = rua;
      data.numero = numero;
      data.complemento = document.getElementById("complemento").value.trim();
      data.telefone = telefone;

      try {
        const response = await fetch("/api/cadastro", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data)
        });

        const result = await response.json();
        if (response.ok) {
          alert("✅ Conta criada com sucesso!");
          window.location.href = "/login";
        } else {
          alert(`⚠️ ${result.message || "Erro ao cadastrar. Verifique os dados."}`);
        }
      } catch (error) {
        console.error("Erro de conexão:", error);
        alert("❌ Erro de conexão com o servidor. Verifique sua internet e tente novamente.");
      } finally {
        if (btnText) btnText.style.display = "block";
        if (btnLoader) btnLoader.style.display = "none";
        submitBtn.disabled = false;
      }
    });
  }
});

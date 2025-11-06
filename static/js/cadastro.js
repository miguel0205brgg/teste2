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

  // 2. Validação de Senha em Tempo Real
  function validarSenhas() {
    if (senhaInput.value && confirmarSenhaInput.value) {
      if (senhaInput.value !== confirmarSenhaInput.value) {
        senhaFeedback.textContent = "As senhas não coincidem.";
        confirmarSenhaInput.setCustomValidity("As senhas não coincidem.");
      } else {
        senhaFeedback.textContent = "";
        confirmarSenhaInput.setCustomValidity("");
      }
    }
  }
  senhaInput.addEventListener("input", validarSenhas);
  confirmarSenhaInput.addEventListener("input", validarSenhas);

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

  async function buscarCep(cep) {
    try {
      const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
      const data = await response.json();

      if (!data.erro) {
        if (ruaInput) ruaInput.value = data.logradouro;
        const numeroInput = document.getElementById("numero");
        if (numeroInput) numeroInput.focus(); // Move o foco para o número
      } else {
        alert("CEP não encontrado.");
        if (ruaInput) ruaInput.value = "";
      }
    } catch (error) {
      console.error("Erro ao buscar CEP:", error);
    }
  }

  // 4. Submissão do Formulário
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      
      if (senhaInput.value !== confirmarSenhaInput.value) {
        alert("As senhas não coincidem! Por favor, verifique.");
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

      const formData = new FormData(form);
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

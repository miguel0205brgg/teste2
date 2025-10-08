document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('cadastroForm');
    const submitBtn = form.querySelector('.submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoader = submitBtn.querySelector('.btn-loader');

    // Função para mostrar erro em um campo específico
    function showError(fieldName, message) {
        const field = document.getElementById(fieldName);
        const errorDiv = document.getElementById(fieldName + '-error');
        
        field.classList.add('error');
        errorDiv.textContent = message;
        errorDiv.classList.add('show');
    }

    // Função para limpar erro de um campo específico
    function clearError(fieldName) {
        const field = document.getElementById(fieldName);
        const errorDiv = document.getElementById(fieldName + '-error');
        
        field.classList.remove('error');
        errorDiv.textContent = '';
        errorDiv.classList.remove('show');
    }

    // Função para limpar todos os erros
    function clearAllErrors() {
        const fields = ['nome', 'email', 'senha', 'telefone', 'cep', 'numero', 'complemento'];
        fields.forEach(field => clearError(field));
    }

    // Função para mostrar loading no botão
    function showLoading() {
        submitBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'block';
    }

    // Função para esconder loading no botão
    function hideLoading() {
        submitBtn.disabled = false;
        btnText.style.display = 'block';
        btnLoader.style.display = 'none';
    }

    // Validação em tempo real
    const inputs = form.querySelectorAll('.form-input');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.value.trim()) {
                clearError(this.name);
            }
        });

        input.addEventListener('blur', function() {
            validateField(this);
        });
    });

    // Função para validar um campo específico
    function validateField(field) {
        const value = field.value.trim();
        const fieldName = field.name;

        switch(fieldName) {
            case 'nome':
                if (!value) {
                    showError(fieldName, 'O campo "nome" é obrigatório e não pode estar vazio.');
                    return false;
                } else if (value.length < 2) {
                    showError(fieldName, 'O nome deve ter pelo menos 2 caracteres.');
                    return false;
                }
                break;

            case 'email':
                if (!value) {
                    showError(fieldName, 'O campo "email" é obrigatório e não pode estar vazio.');
                    return false;
                } else if (!/^[\S+@\S+\.\S+]+$/.test(value)) {
                    showError(fieldName, 'Por favor, digite um e-mail válido.');
                    return false;
                }
                break;

            case 'senha':
                if (!value) {
                    showError(fieldName, 'O campo "senha" é obrigatório e não pode estar vazio.');
                    return false;
                } else if (value.length < 6) {
                    showError(fieldName, 'A senha deve ter pelo menos 6 caracteres.');
                    return false;
                }
                break;

            case 'telefone':
                if (!value) {
                    showError(fieldName, 'O campo "telefone" é obrigatório e não pode estar vazio.');
                    return false;
                } else if (!/^\d{5}-\d{4}$|^\d{4}-\d{4}$|^\d{8}$|^\d{9}$/.test(value.replace(/\D/g, ''))) {
                    showError(fieldName, 'Por favor, digite um telefone válido (ex: (11) 99999-9999).');
                    return false;
                }
                break;

            case 'cep':
                if (!value) {
                    showError(fieldName, 'O campo "CEP" é obrigatório e não pode estar vazio.');
                    return false;
                } else if (!/^\d{5}-\d{3}$/.test(value)) {
                    showError(fieldName, 'Por favor, digite um CEP válido (ex: 12345-678).');
                    return false;
                }
                break;

            case 'numero':
                if (!value) {
                    showError(fieldName, 'O campo "Número" é obrigatório e não pode estar vazio.');
                    return false;
                } else if (value.length > 10) {
                    showError(fieldName, 'O número deve ter no máximo 10 caracteres.');
                    return false;
                }
                break;
            
            case 'complemento':
                if (value && value.length > 30) {
                    showError(fieldName, 'O complemento deve ter no máximo 30 caracteres.');
                    return false;
                }
                break;
        }

        clearError(fieldName);
        return true;
    }

    // Função para validar todo o formulário
    function validateForm() {
        let isValid = true;
        // Validar campos obrigatórios
        const requiredFields = ['nome', 'email', 'senha', 'telefone', 'cep', 'numero'];
        requiredFields.forEach(fieldName => {
            const field = document.getElementById(fieldName);
            if (field && !validateField(field)) {
                isValid = false;
            }
        });

        // Validar campo opcional (complemento)
        const complementoField = document.getElementById('complemento');
        if (complementoField && !validateField(complementoField)) {
            isValid = false;
        }

        return isValid;
    }

    // Submissão do formulário
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        clearAllErrors();
        
        if (!validateForm()) {
            return;
        }

        showLoading();

        const formData = {
            nome: document.getElementById('nome').value.trim(),
            email: document.getElementById('email').value.trim(),
            senha: document.getElementById('senha').value,
            telefone: document.getElementById('telefone').value.trim(),
            cep: document.getElementById('cep').value.trim(),
            numero: document.getElementById('numero').value.trim(),
            complemento: document.getElementById('complemento').value.trim() // Complemento é opcional
        };

        try {
            const response = await fetch('/api/cadastro', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (result.success) {
                // Sucesso - redirecionar ou mostrar mensagem de sucesso
                alert('Cadastro realizado com sucesso! Você será redirecionado para o login.');
                window.location.href = '/login';
            } else {
                // Erro - mostrar mensagem específica
                if (result.field) {
                    showError(result.field, result.message);
                } else {
                    alert('Erro no cadastro: ' + result.message);
                }
            }
        } catch (error) {
            console.error('Erro na requisição:', error);
            alert('Erro de conexão. Tente novamente.');
        } finally {
            hideLoading();
        }
    });

    // Formatação do telefone em tempo real
    const telefoneInput = document.getElementById('telefone');
    telefoneInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        
        if (value.length <= 11) {
            if (value.length <= 2) {
                value = value.replace(/(\d{0,2})/, '($1');
            } else if (value.length <= 6) {
                value = value.replace(/(\d{2})(\d{0,4})/, '($1) $2');
            } else if (value.length <= 10) {
                value = value.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
            } else {
                value = value.replace(/(\d{2})(\d{5})(\d{0,4})/, '($1) $2-$3');
            }
        }
        
        e.target.value = value;
    });

    // Formatação do CEP em tempo real
    const cepInput = document.getElementById('cep');
    cepInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length > 5) {
            value = value.replace(/^(\d{5})(\d)/, '$1-$2');
        }
        e.target.value = value;
    });
});


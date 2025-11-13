document.addEventListener('DOMContentLoaded', function() {
    const valorDividaSpan = document.getElementById('valor-divida');
    const detalhesDividaP = document.getElementById('detalhes-divida');
    const btnPagar = document.getElementById('btn-pagar');
    const mensagemStatusDiv = document.getElementById('mensagem-status');

    let valorDivida = 0;

    // 1. Função para buscar a dívida
    function buscarDivida() {
        fetch('/api/divida')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    valorDivida = data.divida.valor;
                    valorDividaSpan.textContent = `R$ ${valorDivida.toFixed(2).replace('.', ',')}`;
                    detalhesDividaP.textContent = data.divida.detalhes;
                    btnPagar.textContent = `Simular Pagamento (R$ ${valorDivida.toFixed(2).replace('.', ',')})`;
                    btnPagar.disabled = false;
                } else {
                    detalhesDividaP.textContent = 'Não foi possível carregar as informações da dívida.';
                    btnPagar.disabled = true;
                }
            })
            .catch(error => {
                console.error('Erro ao buscar dívida:', error);
                detalhesDividaP.textContent = 'Erro de conexão ao buscar a dívida.';
                btnPagar.disabled = true;
            });
    }

    // 2. Função para simular o pagamento
    function simularPagamento() {
        mensagemStatusDiv.className = 'mensagem-status';
        mensagemStatusDiv.textContent = 'Processando pagamento...';
        btnPagar.disabled = true;

        fetch('/api/pagar-divida', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ valor: valorDivida })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                mensagemStatusDiv.classList.add('sucesso');
                mensagemStatusDiv.textContent = data.message;
                // Em um sistema real, aqui você redirecionaria ou atualizaria a tela
                setTimeout(() => {
                    window.location.href = '/dashboard-usuario';
                }, 3000);
            } else {
                mensagemStatusDiv.classList.add('erro');
                mensagemStatusDiv.textContent = data.message;
                btnPagar.disabled = false;
            }
        })
        .catch(error => {
            console.error('Erro ao simular pagamento:', error);
            mensagemStatusDiv.classList.add('erro');
            mensagemStatusDiv.textContent = 'Erro de conexão ao simular o pagamento.';
            btnPagar.disabled = false;
        });
    }

    // 3. Event Listener para o botão de pagamento
    btnPagar.addEventListener('click', simularPagamento);

    // Inicia a busca pela dívida ao carregar a página
    buscarDivida();
});

// --- Navegação entre seções ---
const navItems = document.querySelectorAll('.nav-item');
const contentSections = document.querySelectorAll('.content-section');

navItems.forEach(item => {
  item.addEventListener('click', () => {
    const targetSection = item.getAttribute('data-section');
    
    // Remove active class from all nav items and sections
    navItems.forEach(nav => nav.classList.remove('active'));
    contentSections.forEach(section => section.classList.remove('active'));
    
    // Add active class to clicked nav item and target section
    item.classList.add('active');
    document.getElementById(targetSection).classList.add('active');
  });
});

// --- Dados de exemplo ---
let livros = [
  { id: 1, titulo: 'Dom Casmurro', autor: 'Machado de Assis', status: 'disponivel' },
  { id: 2, titulo: 'O Cortiço', autor: 'Aluísio Azevedo', status: 'emprestado' },
  { id: 3, titulo: 'Iracema', autor: 'José de Alencar', status: 'disponivel' },
  { id: 4, titulo: 'Memórias Póstumas de Brás Cubas', autor: 'Machado de Assis', status: 'disponivel' }
];

let leitores = [
  { id: 1, nome: 'João Silva', email: 'joao@email.com', telefone: '(11) 99999-9999', endereco: 'Rua A, 123' },
  { id: 2, nome: 'Maria Santos', email: 'maria@email.com', telefone: '(11) 88888-8888', endereco: 'Rua B, 456' },
  { id: 3, nome: 'Pedro Oliveira', email: 'pedro@email.com', telefone: '(11) 77777-7777', endereco: 'Rua C, 789' }
];

let emprestimos = [
  { id: 1, livroId: 2, leitorId: 1, dataDevolucao: '2025-10-20', status: 'ativo' }
];

// --- Funções de renderização ---
function renderLivros(filtro = '') {
  const livrosGrid = document.getElementById('livrosGrid');
  const livrosFiltrados = livros.filter(livro => 
    livro.titulo.toLowerCase().includes(filtro.toLowerCase()) ||
    livro.autor.toLowerCase().includes(filtro.toLowerCase())
  );
  
  const badgeColors = ['orange', 'green', 'purple', 'teal'];
  
  livrosGrid.innerHTML = livrosFiltrados.map((livro, index) => `
    <div class="item-card">
      <h4>${livro.titulo}</h4>
      <p>${livro.autor}</p>
      <div class="item-actions">
        <span class="status-badge ${livro.status === 'disponivel' ? 'status-disponivel' : 'status-emprestado'}">
          ${livro.status === 'disponivel' ? 'DISPONÍVEL' : 'EMPRESTADO'}
        </span>
        <button class="btn-icon btn-edit" onclick="editarLivro(${livro.id})">
          <i class="fas fa-edit"></i>
          <span class="badge badge-${badgeColors[index % badgeColors.length]}">${12 + index}</span>
        </button>
        <button class="btn-remove btn-remove-${badgeColors[index % badgeColors.length]}" onclick="removerLivro(${livro.id})">
          Remover
        </button>
      </div>
    </div>
  `).join('');
}

function renderLeitores() {
  const leitoresGrid = document.getElementById('leitoresGrid');
  const badgeColors = ['orange', 'purple', 'teal'];
  
  leitoresGrid.innerHTML = leitores.map((leitor, index) => `
    <div class="item-card">
      <h4>${leitor.nome}</h4>
      <div class="item-info">
        <div class="item-info-row">
          <i class="fas fa-envelope"></i>
          <span>${leitor.email}</span>
        </div>
        <div class="item-info-row">
          <i class="fas fa-phone"></i>
          <span>${leitor.telefone}</span>
        </div>
        <div class="item-info-row">
          <i class="fas fa-map-marker-alt"></i>
          <span>${leitor.endereco}</span>
        </div>
      </div>
      <div class="item-actions">
        <button class="btn-icon btn-edit" onclick="editarLeitor(${leitor.id})">
          <i class="fas fa-edit"></i>
          <span class="badge badge-${badgeColors[index % badgeColors.length]}">${index + 1}</span>
        </button>
      </div>
    </div>
  `).join('');
}

function renderEmprestimos() {
  const emprestimosGrid = document.getElementById('emprestimosGrid');
  
  emprestimosGrid.innerHTML = emprestimos.map(emprestimo => {
    const livro = livros.find(l => l.id === emprestimo.livroId);
    const leitor = leitores.find(l => l.id === emprestimo.leitorId);
    const dataAtual = new Date();
    const dataDevolucao = new Date(emprestimo.dataDevolucao);
    const atrasado = dataDevolucao < dataAtual;
    
    return `
      <div class="item-card">
        <h4>${livro ? livro.titulo : 'Livro não encontrado'}</h4>
        <div class="item-info">
          <div class="item-info-row">
            <i class="fas fa-user"></i>
            <span>${leitor ? leitor.nome : 'Leitor não encontrado'}</span>
          </div>
          <div class="item-info-row">
            <i class="fas fa-calendar"></i>
            <span>Devolução: ${new Date(emprestimo.dataDevolucao).toLocaleDateString('pt-BR')}</span>
          </div>
        </div>
        <div class="item-actions">
          <span class="status-badge ${atrasado ? 'status-emprestado' : 'status-disponivel'}">
            ${atrasado ? 'ATRASADO' : 'ATIVO'}
          </span>
          <button class="btn-remove btn-remove-green" onclick="devolverLivro(${emprestimo.id})">
            Devolver
          </button>
        </div>
      </div>
    `;
  }).join('');
}

function popularSelectLivros() {
  const select = document.getElementById('emprestimoLivro');
  const livrosDisponiveis = livros.filter(l => l.status === 'disponivel');
  
  select.innerHTML = '<option value="">Selecione um livro</option>' +
    livrosDisponiveis.map(livro => `<option value="${livro.id}">${livro.titulo}</option>`).join('');
}

function popularSelectLeitores() {
  const select = document.getElementById('emprestimoLeitor');
  
  select.innerHTML = '<option value="">Selecione um leitor</option>' +
    leitores.map(leitor => `<option value="${leitor.id}">${leitor.nome}</option>`).join('');
}

// --- Event Listeners para formulários ---
document.getElementById('formLivro').addEventListener('submit', (e) => {
  e.preventDefault();
  
  const titulo = document.getElementById('livroTitulo').value;
  const autor = document.getElementById('livroAutor').value;
  
  const novoLivro = {
    id: livros.length + 1,
    titulo,
    autor,
    status: 'disponivel'
  };
  
  livros.push(novoLivro);
  renderLivros();
  popularSelectLivros();
  atualizarDashboard();
  
  e.target.reset();
  alert('Livro cadastrado com sucesso!');
});

document.getElementById('formLeitor').addEventListener('submit', (e) => {
  e.preventDefault();
  
  const nome = document.getElementById('leitorNome').value;
  const email = document.getElementById('leitorEmail').value;
  const telefone = document.getElementById('leitorTelefone').value;
  const endereco = document.getElementById('leitorEndereco').value;
  
  const novoLeitor = {
    id: leitores.length + 1,
    nome,
    email,
    telefone,
    endereco
  };
  
  leitores.push(novoLeitor);
  renderLeitores();
  popularSelectLeitores();
  atualizarDashboard();
  
  e.target.reset();
  alert('Leitor cadastrado com sucesso!');
});

document.getElementById('formEmprestimo').addEventListener('submit', (e) => {
  e.preventDefault();
  
  const livroId = parseInt(document.getElementById('emprestimoLivro').value);
  const leitorId = parseInt(document.getElementById('emprestimoLeitor').value);
  const dataDevolucao = document.getElementById('emprestimoDataDevolucao').value;
  
  if (!livroId || !leitorId || !dataDevolucao) {
    alert('Por favor, preencha todos os campos!');
    return;
  }
  
  const novoEmprestimo = {
    id: emprestimos.length + 1,
    livroId,
    leitorId,
    dataDevolucao,
    status: 'ativo'
  };
  
  emprestimos.push(novoEmprestimo);
  
  // Atualizar status do livro
  const livro = livros.find(l => l.id === livroId);
  if (livro) {
    livro.status = 'emprestado';
  }
  
  renderEmprestimos();
  renderLivros();
  popularSelectLivros();
  atualizarDashboard();
  
  e.target.reset();
  alert('Empréstimo registrado com sucesso!');
});

// --- Busca de livros ---
document.getElementById('searchLivros').addEventListener('input', (e) => {
  renderLivros(e.target.value);
});

// --- Funções de ação ---
function editarLivro(id) {
  const livro = livros.find(l => l.id === id);
  if (livro) {
    const novoTitulo = prompt('Novo título:', livro.titulo);
    const novoAutor = prompt('Novo autor:', livro.autor);
    
    if (novoTitulo && novoAutor) {
      livro.titulo = novoTitulo;
      livro.autor = novoAutor;
      renderLivros();
      alert('Livro atualizado com sucesso!');
    }
  }
}

function removerLivro(id) {
  if (confirm('Tem certeza que deseja remover este livro?')) {
    livros = livros.filter(l => l.id !== id);
    renderLivros();
    atualizarDashboard();
    alert('Livro removido com sucesso!');
  }
}

function editarLeitor(id) {
  const leitor = leitores.find(l => l.id === id);
  if (leitor) {
    const novoNome = prompt('Novo nome:', leitor.nome);
    const novoEmail = prompt('Novo e-mail:', leitor.email);
    const novoTelefone = prompt('Novo telefone:', leitor.telefone);
    const novoEndereco = prompt('Novo endereço:', leitor.endereco);
    
    if (novoNome && novoEmail && novoTelefone && novoEndereco) {
      leitor.nome = novoNome;
      leitor.email = novoEmail;
      leitor.telefone = novoTelefone;
      leitor.endereco = novoEndereco;
      renderLeitores();
      alert('Leitor atualizado com sucesso!');
    }
  }
}

function devolverLivro(id) {
  if (confirm('Confirmar devolução do livro?')) {
    const emprestimo = emprestimos.find(e => e.id === id);
    if (emprestimo) {
      const livro = livros.find(l => l.id === emprestimo.livroId);
      if (livro) {
        livro.status = 'disponivel';
      }
      
      emprestimos = emprestimos.filter(e => e.id !== id);
      renderEmprestimos();
      renderLivros();
      popularSelectLivros();
      atualizarDashboard();
      alert('Livro devolvido com sucesso!');
    }
  }
}

// --- Atualizar Dashboard ---
function atualizarDashboard() {
  const totalLivros = livros.length;
  const livrosDisponiveis = livros.filter(l => l.status === 'disponivel').length;
  const totalLeitores = leitores.length;
  const emprestimosAtivos = emprestimos.filter(e => e.status === 'ativo').length;
  
  const dataAtual = new Date();
  const emprestimosAtrasados = emprestimos.filter(e => {
    const dataDevolucao = new Date(e.dataDevolucao);
    return dataDevolucao < dataAtual && e.status === 'ativo';
  }).length;
  
  // Atualizar os cards do dashboard
  const statCards = document.querySelectorAll('#dashboard .stat-card');
  if (statCards.length >= 4) {
    statCards[0].querySelector('.stat-number').textContent = totalLivros;
    statCards[0].querySelector('.stat-detail').textContent = `${livrosDisponiveis} disponíveis`;
    statCards[1].querySelector('.stat-number').textContent = totalLeitores;
    statCards[2].querySelector('.stat-number').textContent = emprestimosAtivos;
    statCards[3].querySelector('.stat-number').textContent = emprestimosAtrasados;
  }
}

// --- Inicialização ---
document.addEventListener('DOMContentLoaded', () => {
  renderLivros();
  renderLeitores();
  renderEmprestimos();
  popularSelectLivros();
  popularSelectLeitores();
  atualizarDashboard();
});


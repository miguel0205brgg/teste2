document.addEventListener("DOMContentLoaded", function() {
  // Elementos da navegação
  const navItems = document.querySelectorAll(".nav-item");
  const contentSections = document.querySelectorAll(".content-section");

  // Navegação entre seções
  navItems.forEach(item => {
    item.addEventListener("click", function() {
      const sectionId = this.getAttribute("data-section");
      
      // Remover classe active de todos os items
      navItems.forEach(nav => nav.classList.remove("active"));
      
      // Adicionar classe active ao item clicado
      this.classList.add("active");
      
      // Ocultar todas as seções
      contentSections.forEach(section => section.classList.remove("active"));
      
      // Mostrar a seção selecionada
      const selectedSection = document.getElementById(sectionId);
      if (selectedSection) {
        selectedSection.classList.add("active");
      }
    });
  });

  // Busca em Meus Livros
  const searchMeusLivros = document.getElementById("searchMeusLivros");
  if (searchMeusLivros) {
    searchMeusLivros.addEventListener("input", function() {
      const query = this.value.toLowerCase();
      const meusLivrosGrid = document.getElementById("meusLivrosGrid");
      const items = meusLivrosGrid.querySelectorAll(".item-card");
      
      items.forEach(item => {
        const title = item.querySelector("h4")?.textContent.toLowerCase() || "";
        const author = item.querySelector("p")?.textContent.toLowerCase() || "";
        
        if (title.includes(query) || author.includes(query)) {
          item.style.display = "";
        } else {
          item.style.display = "none";
        }
      });
    });
  }

  // Busca em Livros Disponíveis
  const searchDisponíveis = document.getElementById("searchDisponíveis");
  if (searchDisponíveis) {
    searchDisponíveis.addEventListener("input", function() {
      const query = this.value.toLowerCase();
      const disponíveisGrid = document.getElementById("disponíveisGrid");
      const items = disponíveisGrid.querySelectorAll(".item-card");
      
      items.forEach(item => {
        const title = item.querySelector("h4")?.textContent.toLowerCase() || "";
        const author = item.querySelector("p")?.textContent.toLowerCase() || "";
        
        if (title.includes(query) || author.includes(query)) {
          item.style.display = "";
        } else {
          item.style.display = "none";
        }
      });
    });
  }

  // Filtro por Gênero
  const filterGenero = document.getElementById("filterGenero");
  if (filterGenero) {
    filterGenero.addEventListener("change", function() {
      const selectedGenre = this.value.toLowerCase();
      const disponíveisGrid = document.getElementById("disponíveisGrid");
      const items = disponíveisGrid.querySelectorAll(".item-card");
      
      items.forEach(item => {
        if (!selectedGenre) {
          item.style.display = "";
        } else {
          const genre = item.getAttribute("data-genre")?.toLowerCase() || "";
          if (genre === selectedGenre) {
            item.style.display = "";
          } else {
            item.style.display = "none";
          }
        }
      });
    });
  }

  // Botões de Ação
  const emprestar Buttons = document.querySelectorAll(".btn-emprestar");
  emprestar Buttons.forEach(btn => {
    btn.addEventListener("click", function(e) {
      e.preventDefault();
      const bookTitle = this.closest(".item-card")?.querySelector("h4")?.textContent || "Livro";
      alert(`📚 Você solicitou o empréstimo de "${bookTitle}". Sua solicitação foi registrada!`);
    });
  });

  const avaliarButtons = document.querySelectorAll(".btn-avaliar");
  avaliarButtons.forEach(btn => {
    btn.addEventListener("click", function(e) {
      e.preventDefault();
      const bookTitle = this.closest(".item-card")?.querySelector("h4")?.textContent || "Livro";
      alert(`⭐ Você está avaliando "${bookTitle}". Funcionalidade em desenvolvimento!`);
    });
  });

  const favoritarButtons = document.querySelectorAll(".btn-favoritar");
  favoritarButtons.forEach(btn => {
    btn.addEventListener("click", function(e) {
      e.preventDefault();
      const bookTitle = this.closest(".item-card")?.querySelector("h4")?.textContent || "Livro";
      
      if (this.classList.contains("favorited")) {
        this.classList.remove("favorited");
        this.innerHTML = '<i class="fas fa-heart"></i> Favoritar';
        alert(`💔 Você removeu "${bookTitle}" dos favoritos.`);
      } else {
        this.classList.add("favorited");
        this.innerHTML = '<i class="fas fa-heart"></i> Favoritado';
        alert(`❤️ Você adicionou "${bookTitle}" aos favoritos!`);
      }
    });
  });

  // Carregar dados de exemplo (em produção, isso viria do servidor)
  function loadExampleData() {
    // Dados de exemplo para livros disponíveis
    const exampleBooks = [
      {
        title: "O Senhor dos Anéis",
        author: "J.R.R. Tolkien",
        genre: "ficção",
        status: "disponível"
      },
      {
        title: "1984",
        author: "George Orwell",
        genre: "ficção",
        status: "disponível"
      },
      {
        title: "O Código Da Vinci",
        author: "Dan Brown",
        genre: "mistério",
        status: "disponível"
      },
      {
        title: "Orgulho e Preconceito",
        author: "Jane Austen",
        genre: "romance",
        status: "emprestado"
      }
    ];

    // Renderizar livros disponíveis
    const disponíveisGrid = document.getElementById("disponíveisGrid");
    if (disponíveisGrid && disponíveisGrid.querySelector(".empty-state")) {
      disponíveisGrid.innerHTML = "";
      
      exampleBooks.forEach(book => {
        const bookCard = document.createElement("div");
        bookCard.className = "item-card";
        bookCard.setAttribute("data-genre", book.genre);
        bookCard.innerHTML = `
          <h4>${book.title}</h4>
          <p>${book.author}</p>
          <div class="item-info">
            <div class="item-info-row">
              <i class="fas fa-tag"></i>
              <span>${book.genre.charAt(0).toUpperCase() + book.genre.slice(1)}</span>
            </div>
            <div class="item-info-row">
              <i class="fas fa-check-circle"></i>
              <span class="status-badge status-${book.status}">${book.status.toUpperCase()}</span>
            </div>
          </div>
          <div class="item-actions">
            <button class="btn-action btn-emprestar">
              <i class="fas fa-book"></i> Emprestar
            </button>
            <button class="btn-action btn-avaliar">
              <i class="fas fa-star"></i> Avaliar
            </button>
            <button class="btn-action btn-favoritar">
              <i class="fas fa-heart"></i> Favoritar
            </button>
          </div>
        `;
        disponíveisGrid.appendChild(bookCard);
      });

      // Reattach event listeners para os novos botões
      attachButtonListeners();
    }
  }

  // Função para reattach listeners
  function attachButtonListeners() {
    const emprestar Buttons = document.querySelectorAll(".btn-emprestar");
    emprestar Buttons.forEach(btn => {
      btn.addEventListener("click", function(e) {
        e.preventDefault();
        const bookTitle = this.closest(".item-card")?.querySelector("h4")?.textContent || "Livro";
        alert(`📚 Você solicitou o empréstimo de "${bookTitle}". Sua solicitação foi registrada!`);
      });
    });

    const avaliarButtons = document.querySelectorAll(".btn-avaliar");
    avaliarButtons.forEach(btn => {
      btn.addEventListener("click", function(e) {
        e.preventDefault();
        const bookTitle = this.closest(".item-card")?.querySelector("h4")?.textContent || "Livro";
        alert(`⭐ Você está avaliando "${bookTitle}". Funcionalidade em desenvolvimento!`);
      });
    });

    const favoritarButtons = document.querySelectorAll(".btn-favoritar");
    favoritarButtons.forEach(btn => {
      btn.addEventListener("click", function(e) {
        e.preventDefault();
        const bookTitle = this.closest(".item-card")?.querySelector("h4")?.textContent || "Livro";
        
        if (this.classList.contains("favorited")) {
          this.classList.remove("favorited");
          this.innerHTML = '<i class="fas fa-heart"></i> Favoritar';
          alert(`💔 Você removeu "${bookTitle}" dos favoritos.`);
        } else {
          this.classList.add("favorited");
          this.innerHTML = '<i class="fas fa-heart"></i> Favoritado';
          alert(`❤️ Você adicionou "${bookTitle}" aos favoritos!`);
        }
      });
    });
  }

  // Carregar dados de exemplo ao inicializar
  loadExampleData();
});

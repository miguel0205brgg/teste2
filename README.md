# Sistema de Biblioteca Online

Sistema de gerenciamento inteligente de livros e usuários desenvolvido com Flask e integrado ao Supabase.

## 📚 Sobre o Projeto

Este projeto foi desenvolvido como parte do trabalho acadêmico do curso de Ciências da Computação do Centro Universitário Jorge Amado (UNIJORGE). O sistema permite o cadastro e gerenciamento de usuários e leitores, com diferenciação de papéis entre usuários comuns e desenvolvedores.

### Funcionalidades

- ✅ Cadastro de usuários com validação
- ✅ Sistema de autenticação (login/logout)
- ✅ Diferenciação de papéis (usuário/desenvolvedor)
- ✅ Integração com banco de dados Supabase
- ✅ Interface responsiva e moderna
- ✅ Validação de formulários
- ✅ Hash seguro de senhas

## 🛠️ Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Banco de Dados**: PostgreSQL (Supabase)
- **Autenticação**: Session-based
- **Criptografia**: SHA-256 com salt

## 📋 Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)
- Conta no Supabase

## 🚀 Como Executar

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/sistema-biblioteca.git
cd sistema-biblioteca
```

### 2. Crie e ative o ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto com:
```
SUPABASE_URL=sua_url_do_supabase
SUPABASE_KEY=sua_chave_do_supabase
SECRET_KEY=sua_chave_secreta
DEBUG=True
```

### 5. Execute a aplicação
```bash
python src/main.py
```

A aplicação estará disponível em `http://localhost:5000`

## 📊 Estrutura do Banco de Dados

### Tabela: usuarios
- `id` (SERIAL PRIMARY KEY)
- `nome` (VARCHAR(100) NOT NULL)
- `email` (VARCHAR(100) UNIQUE NOT NULL)
- `senha` (VARCHAR(255) NOT NULL)
- `role` (VARCHAR(20) CHECK: 'usuario' ou 'dev')
- `criado_em` (TIMESTAMP DEFAULT NOW())

### Tabela: leitor
- `id` (SERIAL PRIMARY KEY)
- `usuario_id` (INT UNIQUE REFERENCES usuarios(id))
- `endereco` (VARCHAR(255))
- `telefone` (VARCHAR(20))
- `email` (VARCHAR(100))
- `criado_em` (TIMESTAMP DEFAULT NOW())

## 🔐 Sistema de Autenticação

O sistema implementa autenticação baseada em sessões com:
- Hash seguro de senhas usando SHA-256 com salt
- Diferenciação de papéis (usuário comum vs desenvolvedor)
- Validação de formulários no frontend e backend
- Proteção contra ataques comuns

## 📱 Interface

A interface foi desenvolvida com foco em:
- Design responsivo para dispositivos móveis
- Experiência do usuário intuitiva
- Validação em tempo real
- Feedback visual para ações do usuário
- Gradientes e animações modernas

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

- **Anselmo André Agripino de Jesus**
- **Guilherme Victor Assis de Santana**
- **Igor Santos de Almeida**
- **Miguel Moreira Rodrigues**
- **Ruan Barbosa Araújo**

**Orientador**: Prof. Jailson José dos Santos

---

**Centro Universitário Jorge Amado (UNIJORGE)**  
**Curso de Ciências da Computação**  
**Salvador - BA, 2025**

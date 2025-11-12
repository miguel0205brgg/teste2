from supabase import create_client, Client

# Configuração do Supabase
SUPABASE_URL = "SUA_URL_SUPABASE"
SUPABASE_KEY = "SUA_KEY_SUPABASE"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


class SupabaseClient:
    def __init__(self, supabase: Client):
        self.supabase = supabase

    # Usuário
    def criar_usuario(self, nome: str, email: str, senha: str, perfil: str = "usuario"):
        """Cria um usuário"""
        try:
            result = self.supabase.table("usuario").insert({
                "nome": nome,
                "email": email,
                "senha": senha,
                "perfil": perfil
            }).execute()

            return {
                "success": True,
                "data": result.data[0] if result.data else None,
                "message": "Usuário criado com sucesso"
            }
        except Exception as e:
            return {"success": False, "error": str(e), "message": "Erro ao criar usuário"}

    def autenticar_usuario(self, email: str, senha: str):
        """Autentica usuário pelo email e senha"""
        try:
            result = self.supabase.table("usuario").select("*").eq("email", email).eq("senha", senha).execute()
            if result.data:
                return {"success": True, "message": "Autenticado com sucesso"}
            return {"success": False, "message": "Email ou senha incorretos"}
        except Exception as e:
            return {"success": False, "error": str(e), "message": "Erro ao autenticar usuário"}

    def obter_usuario_por_email(self, email: str):
        """Busca um usuário pelo email"""
        try:
            result = self.supabase.table("usuario").select("id, nome, email, perfil, criado_em").eq("email", email).execute()
            if not result.data:
                return {"success": False, "message": "Usuário não encontrado"}
            return {"success": True, "data": result.data[0], "message": "Usuário encontrado"}
        except Exception as e:
            return {"success": False, "error": str(e), "message": "Erro ao buscar usuário por email"}

    # Endereço
    def criar_endereco(self, cep: str, rua: str, numero: str, complemento: str = None):
        """Cria um endereço"""
        try:
            result = self.supabase.table("enderecos").insert({
                "cep": cep,
                "rua": rua,
                "numero": numero,
                "complemento": complemento
            }).execute()
            return {"success": True, "data": result.data[0] if result.data else None, "message": "Endereço criado"}
        except Exception as e:
            return {"success": False, "error": str(e), "message": "Erro ao criar endereço"}

    # Leitor
    def criar_leitor(self, usuario_id: str, id_endereco: str = None, telefone: str = None, email: str = None, nome: str = None):
        """Cria um registro de leitor vinculado ao usuário e endereço"""
        try:
            result = self.supabase.table("leitor").insert({
                "id_usuario": usuario_id,
                "nome": nome,
                "id_endereco": id_endereco,
                "telefone": telefone,
                "email": email
            }).execute()
            return {"success": True, "data": result.data[0] if result.data else None, "message": "Leitor criado com sucesso"}
        except Exception as e:
            return {"success": False, "error": str(e), "message": "Erro ao criar leitor"}

    # Cadastro completo
    def cadastrar_usuario_completo(self, nome: str, email: str, senha: str, cep: str, rua: str, numero: str, complemento: str = None, telefone: str = None):
        """Cadastra um usuário completo (usuario + leitor + endereco)"""
        id_endereco = None
        usuario_id = None
        try:
            # Criar Endereço
            endereco_result = self.criar_endereco(cep, rua, numero, complemento)
            if not endereco_result['success']:
                return endereco_result
            id_endereco = str(endereco_result['data']['id'])

            # Criar Usuário
            usuario_result = self.criar_usuario(nome, email, senha)
            if not usuario_result['success']:
                # Rollback endereço
                self._rollback_endereco(id_endereco)
                return usuario_result
            usuario_id = str(usuario_result['data']['id'])

            # Criar Leitor
            leitor_result = self.criar_leitor(usuario_id, id_endereco, telefone, email, nome)
            if not leitor_result['success']:
                # Rollback usuário e endereço
                self._rollback_usuario_e_endereco(usuario_id, id_endereco)
                return {"success": False, "error": leitor_result['error'], "message": "Erro ao criar perfil de leitor. Rollback realizado."}

            return {"success": True, "data": {"usuario": usuario_result['data'], "leitor": leitor_result['data']}, "message": "Usuário e leitor cadastrados com sucesso"}

        except Exception as e:
            if usuario_id and id_endereco:
                self._rollback_usuario_e_endereco(usuario_id, id_endereco)
            elif id_endereco:
                self._rollback_endereco(id_endereco)
            return {"success": False, "error": str(e), "message": "Erro ao cadastrar usuário completo"}

    # Rollbacks fictícios (implemente conforme necessário)
    def _rollback_endereco(self, endereco_id: str):
        self.supabase.table("enderecos").delete().eq("id", endereco_id).execute()

    def _rollback_usuario_e_endereco(self, usuario_id: str, endereco_id: str):
        self.supabase.table("leitor").delete().eq("id_usuario", usuario_id).execute()
        self.supabase.table("usuario").delete().eq("id", usuario_id).execute()
        self.supabase.table("enderecos").delete().eq("id", endereco_id).execute()

    # Social login
    def get_user_email_from_token(self, token: str):
        """Exemplo: buscar email do usuário via token"""
        # Implemente conforme sua lógica de social login ou Supabase Auth
        return {"email": "teste@teste.com", "name": "Usuário Google"}

    def sync_social_user(self, email: str, nome: str):
        """Exemplo: sincronizar usuário social"""
        # Aqui você pode usar cadastrar_usuario_completo ou apenas criar usuário/leitor
        return {"success": True, "usuario_id": "123", "email": email}


# Instância para importação
supabase_client = SupabaseClient(supabase)

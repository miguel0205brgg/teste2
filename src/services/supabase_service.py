import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Carrega .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL ou SUPABASE_KEY não foram encontrados no .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class SupabaseClient:
    def __init__(self):
        self.supabase = supabase

    # ---------- Usuário ----------
    def criar_usuario(self, nome: str, email: str, senha: str, perfil: str = "usuario"):
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
        try:
            result = self.supabase.table("usuario").select("*").eq("email", email).eq("senha", senha).execute()
            if not result.data:
                return {"success": False, "message": "Email ou senha incorretos"}
            return {"success": True, "data": result.data[0]}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def obter_usuario_por_email(self, email: str):
        try:
            result = self.supabase.table("usuario").select("*").eq("email", email).execute()
            if not result.data:
                return {"success": False, "message": "Usuário não encontrado"}
            return {"success": True, "data": result.data[0]}
        except Exception as e:
            return {"success": False, "error": str(e), "message": "Erro ao buscar usuário"}

    # ---------- Endereço ----------
    def criar_endereco(self, cep: str, rua: str, numero: str, complemento: str = None):
        try:
            result = self.supabase.table("enderecos").insert({
                "cep": cep,
                "rua": rua,
                "numero": numero,
                "complemento": complemento
            }).execute()
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e), "message": "Erro ao criar endereço"}

    # ---------- Leitor ----------
    def criar_leitor(self, usuario_id: str, id_endereco: str = None, telefone: str = None, email: str = None, nome: str = None):
        try:
            result = self.supabase.table("leitor").insert({
                "id_usuario": usuario_id,
                "nome": nome,
                "id_endereco": id_endereco,
                "telefone": telefone,
                "email": email
            }).execute()
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e), "message": "Erro ao criar leitor"}

    # ---------- Cadastro Completo ----------
    def cadastrar_usuario_completo(self, nome, email, senha, cep, rua, numero, complemento=None, telefone=None):
        """Cadastra usuário + endereço + leitor com rollback automático"""
        id_endereco = None
        usuario_id = None
        try:
            # Criar endereço
            endereco_res = self.criar_endereco(cep, rua, numero, complemento)
            if not endereco_res["success"]:
                return endereco_res
            id_endereco = str(endereco_res["data"]["id"])

            # Criar usuário
            usuario_res = self.criar_usuario(nome, email, senha)
            if not usuario_res["success"]:
                self._rollback_endereco(id_endereco)
                return usuario_res
            usuario_id = str(usuario_res["data"]["id"])

            # Criar leitor
            leitor_res = self.criar_leitor(usuario_id=usuario_id, id_endereco=id_endereco, telefone=telefone, email=email, nome=nome)
            if not leitor_res["success"]:
                self._rollback_usuario_e_endereco(usuario_id, id_endereco)
                return {"success": False, "error": leitor_res.get("error"), "message": "Erro ao criar leitor. Rollback realizado."}

            return {"success": True, "data": {"usuario": usuario_res["data"], "leitor": leitor_res["data"]}}

        except Exception as e:
            if usuario_id and id_endereco:
                self._rollback_usuario_e_endereco(usuario_id, id_endereco)
            elif id_endereco:
                self._rollback_endereco(id_endereco)
            return {"success": False, "error": str(e), "message": "Erro ao cadastrar usuário completo"}

    # ---------- Rollbacks ----------
    def _rollback_endereco(self, id_endereco):
        try:
            self.supabase.table("enderecos").delete().eq("id", id_endereco).execute()
        except:
            pass

    def _rollback_usuario_e_endereco(self, usuario_id, id_endereco):
        try:
            self.supabase.table("leitor").delete().eq("id_usuario", usuario_id).execute()
            self.supabase.table("usuario").delete().eq("id", usuario_id).execute()
            self.supabase.table("enderecos").delete().eq("id", id_endereco).execute()
        except:
            pass

    # ---------- Social/Login Google ----------
    def get_user_email_from_token(self, token):
        # Apenas exemplo; ajuste conforme integração real do Google
        return {"email": "usuario@gmail.com", "name": "Usuário Google"}

    def sync_social_user(self, email, nome):
        usuario = self.obter_usuario_por_email(email)
        if usuario["success"]:
            return {"success": True, "usuario_id": usuario["data"]["id"], "email": usuario["data"]["email"]}
        else:
            # Cria usuário + leitor
            res = self.cadastrar_usuario_completo(nome, email, "senha_provisoria123", "00000-000", "Rua Exemplo", "123")
            if res["success"]:
                return {"success": True, "usuario_id": res["data"]["usuario"]["id"], "email": email}
            return {"success": False, "error": res.get("error", "Erro desconhecido")}

# Instância global para importar em routes
supabase_client = SupabaseClient()

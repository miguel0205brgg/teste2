from supabase import create_client, Client
from src.config import SUPABASE_URL, SUPABASE_KEY
import bcrypt
from datetime import datetime, timedelta
import secrets

class SupabaseService:
    def __init__(self):
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    def hash_password(self, password: str) -> str:
        """Hash da senha usando bcrypt"""
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verifica se a senha está correta usando bcrypt"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except:
            return False
    
    def criar_usuario(self, nome: str, email: str, senha: str = None, role: str = "usuario", supabase_auth_id: str = None):
        """Cria um novo usuário na tabela usuario"""
        try:
            senha_hash = self.hash_password(senha) if senha else None
            
            result = self.supabase.table('usuario').insert({
                'nome': nome,
                'email': email,
                'senha': senha_hash,
                'role': role,
                'supabase_auth_id': supabase_auth_id
            }).execute()
            
            return {
                'success': True,
                'data': result.data[0] if result.data else None,
                'message': 'Usuário criado com sucesso'
            }
        except Exception as e:
            error_message = str(e)
            if "duplicate key value violates unique constraint" in error_message and "email" in error_message:
                return {
                    'success': False,
                    'field': 'email',
                    'message': 'Este e-mail já está cadastrado. Por favor, use outro e-mail.',
                    'error': error_message
                }
            elif "duplicate key value violates unique constraint" in error_message and "supabase_auth_id" in error_message:
                return {
                    'success': False,
                    'field': 'supabase_auth_id',
                    'message': 'Este ID de autenticação Supabase já está em uso.',
                    'error': error_message
                }
            else:
                return {
                    'success': False,
                    'error': error_message,
                    'message': 'Erro ao criar usuário. Verifique os dados e tente novamente.'
                }
    
    def criar_leitor(self, usuario_id: int, endereco: str = None, telefone: str = None, email: str = None):
        """Cria um registro de leitor vinculado ao usuário"""
        try:
            result = self.supabase.table('leitor').insert({
                'id_usuario': usuario_id,
                'endereco': endereco,
                'telefone': telefone,
                'email': email
            }).execute()
            
            return {
                'success': True,
                'data': result.data[0] if result.data else None,
                'message': 'Leitor criado com sucesso'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Erro ao criar leitor'
            }

    def cadastrar_usuario_completo(self, nome: str, email: str, senha: str, endereco: str = None, telefone: str = None):
        """Cadastra um usuário completo (usuario + leitor)"""
        try:
            usuario_result = self.criar_usuario(nome, email, senha=senha, role='usuario', supabase_auth_id=None)            
            if not usuario_result['success']:
                return usuario_result
            
            usuario_id = usuario_result['data']['id']
            leitor_result = self.criar_leitor(usuario_id, endereco, telefone, email)
            
            if not leitor_result['success']:
                self.supabase.table('usuario').delete().eq('id', usuario_id).execute()
                return {
                    'success': False,
                    'error': leitor_result['error'],
                    'message': 'Erro ao criar perfil de leitor'
                }
            
            return {
                'success': True,
                'data': {
                    'usuario': usuario_result['data'],
                    'leitor': leitor_result['data']
                },
                'message': 'Usuário e leitor cadastrados com sucesso'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Erro ao cadastrar usuário completo'
            }
    
    def autenticar_usuario(self, email: str, senha: str):
        """Autentica um usuário pelo email e senha"""
        try:
            result = self.supabase.table('usuario').select('*').eq('email', email).execute()
            
            if not result.data:
                return {
                    'success': False,
                    'field': 'email',
                    'message': 'Usuário não encontrado. Verifique o e-mail digitado.'
                }
            
            usuario = result.data[0]
            
            if self.verify_password(senha, usuario['senha']):
                del usuario['senha']
                return {
                    'success': True,
                    'data': usuario,
                    'message': 'Login realizado com sucesso'
                }
            else:
                return {
                    'success': False,
                    'field': 'senha',
                    'message': 'Senha incorreta. Por favor, tente novamente.'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Erro ao autenticar usuário'
            }

    def autenticar_com_oauth(self, provider: str = "google", redirect_to: str = None):
        """Inicia o fluxo de autenticação OAuth com um provedor específico e retorna a URL de redirecionamento."""
        try:
            auth_url = f"{SUPABASE_URL}/auth/v1/authorize?provider={provider}"
            if redirect_to:
                auth_url += f"&redirect_to={redirect_to}"

            return {
                'success': True,
                'redirect_url': auth_url,
                'message': f'Redirecione o usuário para {auth_url} para iniciar o login com {provider}.'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Erro ao iniciar autenticação OAuth com {provider}.'
            }
    
    def get_or_create_oauth_user(self, email: str, name: str, supabase_auth_id: str):
        """Verifica se um usuário OAuth existe na tabela 'usuario' e o cria se não existir."""
        try:
            existing_user = self.supabase.table("usuario").select("*").eq("email", email).execute()

            if existing_user.data:
                user_data = existing_user.data[0]
                if user_data.get("supabase_auth_id") != supabase_auth_id:
                    self.supabase.table("usuario").update({"supabase_auth_id": supabase_auth_id}).eq("id", user_data["id"]).execute()
                return {"success": True, "data": user_data, "message": "Usuário OAuth encontrado."}
            else:
                new_user_result = self.supabase.table("usuario").insert({
                    "nome": name,
                    "email": email,
                    "role": "usuario",
                    "supabase_auth_id": supabase_auth_id
                }).execute()
                if new_user_result.data:
                    return {"success": True, "data": new_user_result.data[0], "message": "Usuário OAuth criado com sucesso."}
                else:
                    return {"success": False, "message": "Erro ao criar usuário OAuth na tabela local."}
        except Exception as e:
            return {"success": False, "error": str(e), "message": "Erro ao processar usuário OAuth."}

    def buscar_usuario_por_id(self, usuario_id: int):
        """Busca um usuário pelo ID"""
        try:
            result = self.supabase.table('usuario').select('id, nome, email, role, criado_em').eq('id', usuario_id).execute()
            
            if not result.data:
                return {
                    'success': False,
                    'message': 'Usuário não encontrado'
                }
            
            return {
                'success': True,
                'data': result.data[0],
                'message': 'Usuário encontrado'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Erro ao buscar usuário'
            }

    def gerar_token_reset_senha(self, email: str):
        """Gera um token de reset de senha e o armazena na tabela reset_senha"""
        try:
            user_result = self.supabase.table("usuario").select("id").eq("email", email).execute()
            if not user_result.data:
                return {"success": False, "message": "Usuário não encontrado."}
            
            usuario_id = user_result.data[0]["id"]
            token = secrets.token_urlsafe(32)
            expiracao = 3600

            self.supabase.table("reset_senha").delete().eq("id_usuario", usuario_id).execute()

            insert_result = self.supabase.table("reset_senha").insert({
                "id_usuario": usuario_id,
                "token": token,
                "expiracao": expiracao
            }).execute()

            if insert_result.data:
                return {"success": True, "token": token, "message": "Token de reset de senha gerado com sucesso."}
            else:
                return {"success": False, "message": "Erro ao gerar token de reset de senha."}

        except Exception as e:
            return {"success": False, "error": str(e), "message": "Erro interno ao gerar token de reset de senha."}

    def validar_token_reset_senha(self, token: str):
        """Valida um token de reset de senha e retorna o id do usuário se for válido"""
        try:
            result = self.supabase.table("reset_senha").select("id_usuario, expiracao, criado_em").eq("token", token).execute()
            
            if not result.data:
                return {"success": False, "message": "Token inválido ou expirado."}
            
            token_data = result.data[0]
            criado_em = datetime.fromisoformat(token_data["criado_em"].replace("Z", "+00:00"))
            expiracao_segundos = token_data["expiracao"]
            
            if datetime.now(criado_em.tzinfo) > criado_em + timedelta(seconds=expiracao_segundos):
                self.supabase.table("reset_senha").delete().eq("token", token).execute()
                return {"success": False, "message": "Token inválido ou expirado."}
            
            return {"success": True, "id_usuario": token_data["id_usuario"], "message": "Token válido."}

        except Exception as e:
            return {"success": False, "error": str(e), "message": "Erro interno ao validar token de reset de senha."}

    def resetar_senha(self, token: str, nova_senha: str):
        """Reseta a senha do usuário após validação do token"""
        try:
            token_validation = self.validar_token_reset_senha(token)
            if not token_validation["success"]:
                return token_validation
            
            usuario_id = token_validation["id_usuario"]
            senha_hash = self.hash_password(nova_senha)
            
            update_result = self.supabase.table("usuario").update({"senha": senha_hash}).eq("id", usuario_id).execute()
            
            if update_result.data:
                self.supabase.table("reset_senha").delete().eq("token", token).execute()
                return {"success": True, "message": "Senha resetada com sucesso."}
            else:
                return {"success": False, "message": "Erro ao resetar a senha."}

        except Exception as e:
            return {"success": False, "error": str(e), "message": "Erro interno ao resetar a senha."}

from supabase import create_client, Client
from src.config import SUPABASE_URL, SUPABASE_KEY
import hashlib
import secrets
from datetime import datetime, timedelta

class SupabaseService:
    def __init__(self):
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    def hash_password(self, password: str) -> str:
        """Hash da senha usando SHA-256 com salt"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}:{password_hash}"
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verifica se a senha está correta"""
        try:
            salt, password_hash = hashed.split(":")
            return hashlib.sha256((password + salt).encode()).hexdigest() == password_hash
        except:
            return False
    
    def criar_usuario(self, nome: str, email: str, senha: str, perfil: str = "usuario"):
        """Cria um novo usuário na tabela usuario"""
        print(f"[DEBUG SUPABASE] Tentando criar usuário: nome={nome}, email={email}, perfil={perfil}")
        try:
            senha_hash = self.hash_password(senha)
            
            result = self.supabase.table('usuario').insert({
                'nome': nome,
                'email': email,
                'senha': senha_hash,
                'perfil': perfil
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
            return {
                'success': False,
                'error': error_message,
                'message': 'Erro ao criar usuário. Verifique os dados e tente novamente.'
            }
    
    def criar_leitor(self, usuario_id: int, endereco: str = None, telefone: str = None, email: str = None):
        """Cria um registro de leitor vinculado ao usuário"""
        print(f"[DEBUG SUPABASE] Tentando criar leitor: usuario_id={usuario_id}, endereco={endereco}, telefone={telefone}, email={email}")
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
        """Cadastra um usuário completo (usuario + leitor se for tipo 'usuario')"""
        try:
            usuario_result = self.criar_usuario(nome, email, senha, perfil='usuario')
            
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
            
            if self.verify_password(senha, usuario["senha"]):
                del usuario["senha"]
                return {
                    "success": True,
                    "data": usuario,
                    "message": "Login realizado com sucesso"
                }
            else:
                return {
                    "success": False,
                    "field": "senha",
                    "message": "Senha incorreta. Por favor, tente novamente."
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Erro ao autenticar usuário'
            }
    
    def buscar_usuario_por_id(self, usuario_id: int):
        """Busca um usuário pelo ID"""
        try:
            result = self.supabase.table("usuario").select("id, nome, email, perfil, criado_em").eq("id", usuario_id).execute()
            
            if not result.data:
                return {
                    "success": False,
                    "message": "Usuário não encontrado"
                }
            
            return {
                "success": True,
                "data": result.data[0],
                "message": "Usuário encontrado"
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Erro ao buscar usuário'
            }

    def atualizar_usuario(self, usuario_id: int, nome: str = None, email: str = None):
        """Atualiza os dados do usuário (nome e/ou email)"""
        print(f"[DEBUG SUPABASE] Tentando atualizar usuário: usuario_id={usuario_id}, nome={nome}, email={email}")
        try:
            # Preparar dados a atualizar
            dados_atualizacao = {}
            
            if nome:
                dados_atualizacao['nome'] = nome
            
            if email:
                dados_atualizacao['email'] = email
            
            if not dados_atualizacao:
                return {
                    'success': False,
                    'message': 'Nenhum dado para atualizar'
                }
            
            # Atualizar usuário no banco de dados
            result = self.supabase.table('usuario').update(dados_atualizacao).eq('id', usuario_id).execute()
            
            if result.data:
                return {
                    'success': True,
                    'data': result.data[0] if result.data else None,
                    'message': 'Usuário atualizado com sucesso'
                }
            else:
                return {
                    'success': False,
                    'message': 'Erro ao atualizar usuário'
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
            return {
                'success': False,
                'error': error_message,
                'message': 'Erro ao atualizar usuário'
            }

    def gerar_token_reset_senha(self, email: str):
        """Gera um token de reset de senha e o armazena na tabela reset_senha"""
        try:
            user_result = self.supabase.table("usuario").select("id").eq("email", email).execute()
            if not user_result.data:
                return {
                    "success": False,
                    "message": "Usuário não encontrado."
                }
            
            usuario_id = user_result.data[0]["id"]
            token = secrets.token_urlsafe(32)
            expiracao = datetime.now() + timedelta(hours=1) # Expira em 1 hora

            self.supabase.table("reset_senha").delete().eq("id_usuario", usuario_id).execute()

            insert_result = self.supabase.table("reset_senha").insert({
                "id_usuario": usuario_id,
                "token": token,
                "expiracao": expiracao
            }).execute()

            if insert_result.data:
                return {
                    "success": True,
                    "token": token,
                    "message": "Token de reset de senha gerado com sucesso."
                }
            else:
                return {
                    "success": False,
                    "message": "Erro ao gerar token de reset de senha."
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Erro interno ao gerar token de reset de senha."
            }

    def validar_token_reset_senha(self, token: str):
        """Valida um token de reset de senha e retorna o id do usuário se for válido"""
        try:
            result = self.supabase.table("reset_senha").select("id_usuario, expiracao, criado_em").eq("token", token).execute()
            
            if not result.data:
                return {
                    "success": False,
                    "message": "Token inválido ou expirado."
                }
            
            token_data = result.data[0]
            criado_em_str = token_data["criado_em"]
            criado_em = datetime.fromisoformat(criado_em_str.replace("Z", "+00:00"))
            expiracao_segundos = token_data["expiracao"]
            
            if datetime.now(criado_em.tzinfo) > criado_em + timedelta(seconds=expiracao_segundos):
                self.supabase.table("reset_senha").delete().eq("token", token).execute()
                return {
                    "success": False,
                    "message": "Token inválido ou expirado."
                }
            
            return {
                "success": True,
                "id_usuario": token_data["id_usuario"],
                "message": "Token válido."
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Erro interno ao validar token de reset de senha."
            }

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
                return {
                    "success": True,
                    "message": "Senha resetada com sucesso."
                }
            else:
                return {
                    "success": False,
                    "message": "Erro ao resetar a senha."
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Erro interno ao resetar a senha."
            }

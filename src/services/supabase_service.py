from supabase import create_client, Client
from src.config import SUPABASE_URL, SUPABASE_KEY
import hashlib
import secrets

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
            salt, password_hash = hashed.split(':')
            return hashlib.sha256((password + salt).encode()).hexdigest() == password_hash
        except:
            return False
    
    def criar_usuario(self, nome: str, email: str, senha: str, role: str = 'usuario'):
        """Cria um novo usuário na tabela usuario"""
        try:
            # Hash da senha
            senha_hash = self.hash_password(senha)
            
            # Inserir usuário
            result = self.supabase.table('usuario').insert({
                'nome': nome,
                'email': email,
                'senha': senha_hash,
                'role': role
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
    
    def cadastrar_usuario_completo(self, nome: str, email: str, senha: str, 
                                 endereco: str = None, telefone: str = None):
        """Cadastra um usuário completo (usuario + leitor se for tipo 'usuario')"""
        try:
            # Criar usuário
            usuario_result = self.criar_usuario(nome, email, senha, role='usuario')
            
            if not usuario_result['success']:
                return usuario_result
            
            usuario_id = usuario_result['data']['id']
            
            # Se for usuário comum, criar também o registro de leitor
            # A role é sempre 'usuario' agora, então esta condição é sempre verdadeira
            leitor_result = self.criar_leitor(usuario_id, endereco, telefone, email)
            
            if not leitor_result['success']:
                # Se falhar ao criar leitor, remover o usuário criado
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
            # Buscar usuário pelo email
            result = self.supabase.table('usuario').select('*').eq('email', email).execute()
            
            if not result.data:
                return {
                    'success': False,
                    'field': 'email',
                    'message': 'Usuário não encontrado. Verifique o e-mail digitado.'
                }
            
            usuario = result.data[0]
            
            # Verificar senha
            if self.verify_password(senha, usuario['senha']):
                # Remover senha do retorno
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
            # Buscar usuário pelo email
            user_result = self.supabase.table("usuario").select("id").eq("email", email).execute()
            if not user_result.data:
                return {
                    "success": False,
                    "message": "Usuário não encontrado."
                }
            
            usuario_id = user_result.data[0]["id"]
            token = secrets.token_urlsafe(32) # Gera um token seguro
            expiracao = 3600 # Token válido por 1 hora (3600 segundos)

            # Inserir ou atualizar o token na tabela reset_senha
            # Primeiro, tentar deletar tokens antigos para o mesmo usuário
            self.supabase.table("reset_senha").delete().eq("id_usuario", usuario_id).execute()

            # Inserir novo token
            insert_result = self.supabase.table("reset_senha").insert({
                "id_usuario": usuario_id,
                "token": token,
                "expiracao": expiracao # Armazenar como timestamp ou tempo de vida
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
            # Buscar token na tabela reset_senha
            result = self.supabase.table("reset_senha").select("id_usuario, expiracao, criado_em").eq("token", token).execute()
            
            if not result.data:
                return {
                    "success": False,
                    "message": "Token inválido ou expirado."
                }
            
            token_data = result.data[0]
            criado_em_str = token_data["criado_em"]
            # Supondo que 'criado_em' é um timestamp ISO 8601
            from datetime import datetime, timedelta
            criado_em = datetime.fromisoformat(criado_em_str.replace("Z", "+00:00")) # Ajuste para formato ISO 8601 com fuso horário
            expiracao_segundos = token_data["expiracao"]
            
            # Verificar se o token expirou
            if datetime.now(criado_em.tzinfo) > criado_em + timedelta(seconds=expiracao_segundos):
                # Opcional: remover token expirado
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
            # Validar o token
            token_validation = self.validar_token_reset_senha(token)
            if not token_validation["success"]:
                return token_validation
            
            usuario_id = token_validation["id_usuario"]
            
            # Hash da nova senha
            senha_hash = self.hash_password(nova_senha)
            
            # Atualizar a senha do usuário
            update_result = self.supabase.table("usuario").update({"senha": senha_hash}).eq("id", usuario_id).execute()
            
            if update_result.data:
                # Remover o token de reset de senha após o uso
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


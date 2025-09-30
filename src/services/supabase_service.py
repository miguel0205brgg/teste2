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
        """Cria um novo usuário na tabela usuarios"""
        try:
            # Hash da senha
            senha_hash = self.hash_password(senha)
            
            # Inserir usuário
            result = self.supabase.table('usuarios').insert({
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
                'usuario_id': usuario_id,
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
    
    def cadastrar_usuario_completo(self, nome: str, email: str, senha: str, role: str = 'usuario', 
                                 endereco: str = None, telefone: str = None):
        """Cadastra um usuário completo (usuario + leitor se for tipo 'usuario')"""
        try:
            # Criar usuário
            usuario_result = self.criar_usuario(nome, email, senha, role)
            
            if not usuario_result['success']:
                return usuario_result
            
            usuario_id = usuario_result['data']['id']
            
            # Se for usuário comum, criar também o registro de leitor
            if role == 'usuario':
                leitor_result = self.criar_leitor(usuario_id, endereco, telefone, email)
                
                if not leitor_result['success']:
                    # Se falhar ao criar leitor, remover o usuário criado
                    self.supabase.table('usuarios').delete().eq('id', usuario_id).execute()
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
            
            return usuario_result
            
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
            result = self.supabase.table('usuarios').select('*').eq('email', email).execute()
            
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
            result = self.supabase.table('usuarios').select('id, nome, email, role, criado_em').eq('id', usuario_id).execute()
            
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

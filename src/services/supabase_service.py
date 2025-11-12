# ... código inicial permanece igual ...

    def criar_leitor(self, usuario_id: str, id_endereco: str = None, telefone: str = None, email: str = None, nome: str = None):
        """Cria um registro de leitor vinculado ao usuário e endereço"""
        print(f"[DEBUG SUPABASE] Tentando criar leitor: usuario_id={usuario_id}, nome={nome}, id_endereco={id_endereco}, telefone={telefone}, email={email}")
        try:
            result = self.supabase.table('leitor').insert({
                'id_usuario': usuario_id,
                'nome': nome,
                'id_endereco': id_endereco,
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

    def cadastrar_usuario_completo(self, nome: str, email: str, senha: str, cep: str, rua: str, numero: str, complemento: str = None, telefone: str = None):
        """Cadastra um usuário completo (usuario + leitor + endereco)"""
        id_endereco = None
        usuario_id = None
        
        try:
            # 1. Criar Endereço
            endereco_result = self.criar_endereco(cep, rua, numero, complemento)
            if not endereco_result['success']:
                return endereco_result
            
            id_endereco = str(endereco_result['data']['id'])

            # 2. Criar Usuário
            usuario_result = self.criar_usuario(nome, email, senha, perfil='usuario')
            if not usuario_result['success']:
                # Rollback do endereço
                self._rollback_endereco(id_endereco)
                return usuario_result
            
            usuario_id = str(usuario_result['data']['id'])

            # 3. Criar Leitor
            leitor_result = self.criar_leitor(usuario_id=usuario_id, id_endereco=id_endereco, telefone=telefone, email=email, nome=nome)
            
            if not leitor_result['success']:
                # Rollback do usuário e endereço
                self._rollback_usuario_e_endereco(usuario_id, id_endereco)
                return {
                    'success': False,
                    'error': leitor_result['error'],
                    'message': 'Erro ao criar perfil de leitor. Rollback realizado.'
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
            # Rollback em caso de erro inesperado
            if usuario_id and id_endereco:
                self._rollback_usuario_e_endereco(usuario_id, id_endereco)
            elif id_endereco:
                self._rollback_endereco(id_endereco)
            
            return {
                'success': False,
                'error': str(e),
                'message': 'Erro ao cadastrar usuário completo'
            }

# Remover duplicidade de obter_usuario_por_email
# A função final válida:
def obter_usuario_por_email(self, email: str):
    """Busca um usuário pelo email"""
    try:
        result = self.supabase.table("usuario").select("id, nome, email, perfil, criado_em").eq("email", email).execute()
        
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
            'message': 'Erro ao buscar usuário por email'
        }

# ... restante do código permanece igual ...

from apis.entidades import *

alunos = api_entidades["alunos"]
turmas = api_entidades['turmas']

class AlunoNaoEncontrado(Exception):
    pass

def listar_alunos():
    return alunos

def aluno_por_id(id_aluno):
    for aluno in alunos:
        if aluno["id"] == id_aluno:
            return aluno
    raise AlunoNaoEncontrado

def adicionar_aluno(novo_aluno):    
    if not turmas:
        raise AlunoNaoEncontrado
    
    if not novo_aluno.get('id'):
        novo_aluno['id'] = alunos[-1]["id"] + 1 if alunos else 1   
    if not novo_aluno.get("nome"):
        return "aluno sem nome"
    if not novo_aluno.get("nota_primeiro_semestre"):
        return "aluno sem primeira nota"
    if novo_aluno['nota_primeiro_semestre'] > 10 or novo_aluno['nota_primeiro_semestre'] < 0:
        return 'Nota primeiro semestre inválida'
    if not novo_aluno.get("nota_segundo_semestre"):
        return "aluno sem segunda nota"
    if novo_aluno['nota_segundo_semestre'] > 10 or novo_aluno['nota_segundo_semestre'] < 0:
        return 'Nota segundo semestre inválida'
    if not novo_aluno.get("turma_id"):
        return "aluno sem turma"
    else:
        if not any(turma["id"] == novo_aluno["turma_id"] for turma in turmas):
            return "Id da turma não encontrado"
    if novo_aluno.get("data_nascimento"):
        split = novo_aluno.get("data_nascimento").split('/')
        if not len(split[0]) == 4:
            return "formato da data incorreto, passe no formato 'YYYY/MM/DD"
    else:
         return "aluno sem data de nascimento"
    if not any(aluno["id"] == novo_aluno["id"] for aluno in alunos):
        obj_aluno = Aluno(novo_aluno["id"], novo_aluno['nome'], novo_aluno['data_nascimento'], novo_aluno['nota_primeiro_semestre'], novo_aluno['nota_segundo_semestre'], novo_aluno['turma_id'])
        alunos.append(obj_aluno.converter_aluno_dici())
        return "criado com sucesso"

def atualizar_aluno(id_aluno, novos_dados):
    aluno = aluno_por_id(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado
    
    if not novos_dados.get("nome"):
        return "aluno sem nome"
    aluno["nome"] = novos_dados["nome"]
    if novos_dados.get("data_nascimento"):
        aluno['data_nascimento'] = novos_dados['data_nascimento']
        aluno['idade'] = atribuir_idade(aluno['data_nascimento'])
    if novos_dados.get("nota_primeiro_semestre"):
        if 0 <= novos_dados['nota_primeiro_semestre'] <= 10:
            aluno['nota_primeiro_semestre'] = novos_dados['nota_primeiro_semestre']
        else:
            return 'Nota primeiro semestre inválida'
    if novos_dados.get("nota_segundo_semestre"):
        if 0 <= novos_dados['nota_segundo_semestre'] <= 10:
            aluno['nota_segundo_semestre'] = novos_dados['nota_segundo_semestre']
        else:
            return 'Nota segundo semestre inválida'
        aluno['nota_segundo_semestre'] = novos_dados['nota_segundo_semestre']
    if novos_dados.get("turma_id"):
        if any(turma["id"] == novos_dados["turma_id"] for turma in turmas):                                        
            aluno["turma_id"] = novos_dados["turma_id"]
        else:
            return "Id da turma não encontrado"           
    aluno['media_final'] = media(aluno['nota_primeiro_semestre'], aluno['nota_segundo_semestre'] )
    return "atualizado com sucesso"

def excluir_aluno(id_aluno):
    aluno = aluno_por_id(id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado
    alunos.remove(aluno)

from datetime import datetime

class DataException(Exception):
    pass

def calcular_idade(data_nascimento):
    hoje = datetime.now().date()
    nascimento = datetime.strptime(data_nascimento, '%Y/%m/%d').date()
    return hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))

def verificar_data(data_nascimento):
    data = data_nascimento.split("/")
    if len(data) != 3 or len(data[0]) != 4 or len(data[1]) > 2 or len(data[2]) > 2:
        raise DataException("Formato da data incorreto, passe no formato 'YYYY/MM/DD'")
    try:
        ano, mes, dia = int(data[0]), int(data[1]), int(data[2])
        if not (1 <= mes <= 12):
            raise DataException("Mes invalido")
        elif not (1 <= dia <= 31):
            raise DataException("Dia invalido")
        return True
    except ValueError:
        raise DataException("A data de nascimento deve conter apenas numeros")

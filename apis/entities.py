import datetime
def dateAge(birthDate):
    date = birthDate.split("/")
    year = 0
    if len(date[0]) == 4:
        year = int(date[0])
    else:
        return "Digitação da data inesperada" 
    month = int(date[1])
    day = int(date[2])
    dateToday = datetime.date.today()
    if month < int(dateToday.month):
        idade = dateToday.year - year
    elif month == dateToday.month:
        if day <= dateToday.day:
            idade = dateToday.year - year
        else:
            idade = (dateToday.year - year) - 1
    else:
        idade = (dateToday.year - year) - 1
    return idade

api_entidades =  {
    "alunos": [
        {
            "id": 100,
            "nome": "Felipe Santos",
            "idade": 22, 
            "data_nascimento": "2003/02/15", 
            "nota_primeiro_semestre": 10.0, 
            "nota_segundo_semestre": 10.0, 
            "media_final": 10.0,
            "turma_id": 100, 
        }
    ],

    "professores": [
        {
            "id": 100,
            "nome": "João Augusto",
            "idade": 49,
            "data_nascimento": "1975/10/20",
            "disciplina": "Desenvolvimento Web",
            "salario": 5000.0
        }
    ],

    "turmas": [
        {
            "id": 100,
            "nome": "ADS",
            "turno": "Noite",
            "professor_id": 100
        }
    ]
} 

print(dateAge(api_entidades["professores"][0]["data_nascimento"])) 
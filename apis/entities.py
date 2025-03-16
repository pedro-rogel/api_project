import json

api_entidades =  {
    "students": [
    {
        "id": 1,
        "name": "Felippe", 
    },
    {
        "id": 2,
        "name": "Fernando",
    },
    {
        "id": 3,
        "name": "Gustavo",
    },
    {
        "id": 4,
        "name": "Murillo",
    },
    {
        "id": 5,
        "name": "Pedro",
    }],


    "professors": [
    {
        "id": 1,
        "name": "João", 
    },
    {
        "id": 2,
        "name": "Mário",
    },
    {
        "id": 3,
        "name": "Antônio",
    }],


    "classes": [
    {
        "id": 1,
        "name": "ADS", 
    },
    {
        "id": 2,
        "name": "SI",
    },
    ]
}

def output_formatted():
    return json.dumps(api_entidades, indent=4, ensure_ascii=False)

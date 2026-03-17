from core.firebase import db

urnas = [

    {
        "nome": "Urna Luxo Mogno",
        "preco": 3500,
        "descricao": "Urna funerária madeira nobre",
        "imagem": "https://meusite.com/imagens/urna1.jpg",
        "ativo": True
    },

    {
        "nome": "Urna Premium Branco",
        "preco": 4200,
        "descricao": "Urna premium acabamento branco",
        "imagem": "https://meusite.com/imagens/urna2.jpg",
        "ativo": True
    }

]

for urna in urnas:

    db.collection("urnas").add(urna)

    print("Urna criada:", urna["nome"])
import random

lista_de_desculpas = [
    "Me desculpe, mas fui atacado por uma revoada de pombos a caminho da faculdade e estou em recuperação.",
    "Desculpe, mas hoje é o dia mundial da preguiça e eu sou um ativista entusiasta.",
    "Acordei com uma súbita alergia a aulas hoje. É uma condição sazonal, aparentemente.",
    "Desculpe, mas hoje é o aniversário do meu gato e ele estava me implorando para ficar em casa e comemorar com ele.",
    "Fui vítima de um ataque surpresa de preguiça aguda e, infelizmente, perdi a batalha.",
    "Desculpe, professor, mas meu despertador se aposentou e eu ainda não consegui encontrar um substituto adequado.",
    "Houve um contratempo com meu animal de estimação. Meu gato ficou preso no interior do painel do carro e preciso resolver essa situação urgentemente.",
    "O médico recomendou que eu aumentasse minha exposição à vitamina D, então decidi tirar um dia para ir à praia.",
    "Desculpe, não poderei comparecer hoje, minha avó me envenenou com presunto e preciso monitorar minha saúde.",
    "Infelizmente, estou preso em um dilema moral. Meu hamster fugiu e estou em uma missão de resgate para trazê-lo de volta ao lar.",
    "Desculpe, mas hoje é o dia internacional do 'coloque seus pés para cima e relaxe', e eu estou levando isso muito a sério.",
    "Meu uniforme pegou fogo quando o coloquei para secar no microondas.",
    "Acidentalmente, entrei num avião.",
    "Fui testemunhar sobre um traficante de drogas e um amigo dele me assaltou.",
    "Queimei as axilas com um removedor de pelos. Não consigo abaixar os braços.",
    "A panela de pressão explodiu e a minha irmã ficou assustada, preciso cuidar dela.",
    "Preciso ir a um funeral. Vou carregar o caixão do animal de estimação do primo da minha esposa.",
    "Meu cachorro engoliu as chaves do carro, e estou esperando que elas saiam"
]

def gerar_desculpa_por_faltar_na_aula_do_gabriel() -> str:
    return random.choice(lista_de_desculpas)


def gerar_desculpa_por_faltar_na_aula_do_gabriel_cli():
    print(random.choice(lista_de_desculpas))
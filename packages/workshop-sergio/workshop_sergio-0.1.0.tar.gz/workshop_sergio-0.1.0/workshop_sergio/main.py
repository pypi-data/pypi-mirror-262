import random

def desculpa_para_faltar_na_aula():
    desculpas = [
        "Meu cachorro comeu meu caderno de anotações.",
        "Fiquei preso no trânsito por causa de um acidente.",
        "Estou me sentindo um pouco doente e prefiro não contagiar os outros.",
        "Tive um problema familiar urgente para resolver.",
        "Meu despertador não tocou e acabei dormindo demais.",
        "Estou participando de uma competição importante e preciso me preparar.",
        "Perdi meu transporte e não consigo chegar a tempo para a aula.",
        "Preciso comparecer a uma consulta médica que não pode ser adiada.",
        "Estou enfrentando problemas técnicos com meu computador e não consigo acessar as aulas online."
    ]
    return random.choice(desculpas)

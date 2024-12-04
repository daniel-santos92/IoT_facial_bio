import re

def validar_cpf(cpf):
    """
    Valida se o CPF é composto exatamente por 11 dígitos.
    :param cpf: String contendo o CPF a ser validado.
    :return: True se o CPF for válido, False caso contrário.
    """
    return re.match(r"^\d{11}$", cpf) is not None

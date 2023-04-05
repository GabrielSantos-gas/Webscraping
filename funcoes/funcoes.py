import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def trata_porcentagem(porcentagem_str):
    try:
        return locale.atof(porcentagem_str.split('%')[0])
    except ValueError:
        return None

def trata_decimal(decimal_str):
    return locale.atof(decimal_str)

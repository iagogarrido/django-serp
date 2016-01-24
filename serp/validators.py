import locale
from django.core.validators import RegexValidator


validate_bic = RegexValidator(regex="([a-zA-Z]{4}[a-zA-Z]{2}[a-zA-Z0-9]{2}([a-zA-Z0-9]{3})?)",
                              message="Código BIC inválido")

validate_iban = RegexValidator(regex="[a-zA-Z]{2}[0-9]{2}[a-zA-Z0-9]{4}[0-9]{7}([a-zA-Z0-9]?){0,16}",
                               message="Número IBAN inválido")


def validate_nif(value):
    lang_code = locale.getlocale()[0]

    if lang_code == 'es_ES':
        validator = RegexValidator(
            regex="^(X(-|\.)?0?\d{7}(-|\.)?[A-Z]|[A-Z](-|\.)?\d{7}(-|\.)?[0-9A-Z]|\d{8}(-|\.)?[A-Z])$",
            message="NIF inválido")
    else:
        # TODO: añadir validadores del número de identificación para el resto de paises
        return

    validator(value)


def validate_codpostal(value):
    lang_code = locale.getlocale()[0]

    if lang_code == 'es_ES':
        validator = RegexValidator(
            regex="^[0-9]{5}$",
            message="Cod. postal inválido")
    else:
        # TODO: añadir validadores del código postal para el resto de paises
        return

    validator(value)

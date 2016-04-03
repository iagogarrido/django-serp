import datetime
import os
import uuid

from django.http import HttpResponse


__all__ = ['generate_content']


# SEPA releated tools dir
SEPA_DIR = os.path.dirname(__file__)


def generate_content(domiciliacion, empresa, fecha, descripcion, importe):
    with open(os.path.join(SEPA_DIR, 'base.xml'), 'r') as file_sepa:
        base_content = file_sepa.read()

    data = {'MsgId': uuid.uuid4(),
            'CreDtTm': datetime.datetime.now().strftime("%Y-%m-%d"),
            'NbOfTxs': 1, 'CtrlSum': importe, 'PresNm': empresa.nombre,
            'PresId': empresa.nif,
            'PmtInfId': domiciliacion.referencia + "/" + empresa.nif,
            'PmtMtd': "DD", 'ReqdExctnDt': fecha.strftime("%Y-%m-%d"),
            'DbtrNm': domiciliacion.dbtr_nombre, 'DbtrCtry': "ES",
            'DbtrAdrLine': domiciliacion.dbtr_direccion,
            'DbtrAdrLine2': build_adrline2(domiciliacion),
            'DbtrId': domiciliacion.dbtr_nif,
            'DbtrIBAN': domiciliacion.dbtr_iban, 'DbtrCcy': "EUR",
            'DbtrBIC': domiciliacion.dbtr_bic,
            'PmtId': domiciliacion.referencia, 'InstdAmt': importe,
            'CdtrId': empresa.nif, 'CdtrIBAN': empresa.iban,
            'RmtInf': descripcion}

    content = base_content.format_map(data)

    response = HttpResponse(content_type="text/xml")
    response.content = content

    return response


def build_adrline2(domiciliacion):
    return "(" + domiciliacion.dbtr_codpostal + ") "\
           + domiciliacion.dbtr_poblacion + " - "\
           + domiciliacion.dbtr_provincia

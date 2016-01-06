import json

from django.http import JsonResponse

from serp import models


__all__ = ['generate_content']

# SEPA releated tools dir
SEPA_DIR = ''


def generate_content(data):
    return JsonResponse(data)

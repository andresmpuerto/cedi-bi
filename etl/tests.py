import pytest
from django.conf import settings
from django.db import IntegrityError

from account.models import Rol
from analytics.models import Board, TypeBoard
from etl.transform.validate import ValidateCsv


@pytest.mark.django_db
@pytest.mark.parametrize(
    'separator, result', [
        (None, False),
        (':', False),
        ('-', False),
        (';', True),
    ]
)
def test_validate_csv(separator, result):
    validate = ValidateCsv(str(settings.ROOT_DIR)+'\\csv\\template.csv',
                           separator,
                           1, 10000)
    assert validate.is_separator() == result


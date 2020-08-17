import pytest
from django.db import IntegrityError

from account.models import Rol
from analytics.models import Board, TypeBoard


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, count', [
        (None, 0),
        ('Tablero 1', 1),
    ]
)
def test_board_create(name, count):
    try:
        type = TypeBoard()
        type.name = 'Ocupacion'
        type.code = 10
        type.save()

        rol = Rol()
        rol.name = 'Test'
        rol.code = '10'
        rol.save()

        board = Board()
        board.name = name
        board.description = ''
        board.type = type
        board.save()
        board.rol.add(rol)

        assert TypeBoard.objects.count() == count
        assert Rol.objects.count() == count
        assert Board.objects.count() == count

    except IntegrityError as e:
        assert 'null' in str(e)

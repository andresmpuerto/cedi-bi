import json
import pytest
import uuid

from django.conf import settings
from django.core.files import File
from django.db import IntegrityError
from django.urls import reverse
from oauth2_provider.models import get_application_model, AccessToken, RefreshToken
from oauth2_provider.settings import oauth2_settings
from account.models import Company, User, Profile, Rol

Application = get_application_model()
user_test = None


def pretty_print_request(request):
    print('\n{}\n{}\n\n{}\n\n{}\n'.format(
        '-----------Request----------->',
        request.method + ' ' + request.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in request.headers.items()),
        request.body)
    )


def pretty_print_response(response):
    print('{}\n{}\n{}'.format(
        '<-----------Response-----------',
        'Status code:' + str(response.status_code),
        response.content)
    )


@pytest.fixture
def test_password():
    return 'strong-test-pass'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return User.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def get_application(db, create_user):
    user_test = create_user(username='test', email='lennon@thebeatles.com')
    application = Application(
        name="Test Application",
        redirect_uris="http://localhost",
        user=user_test,
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
    )
    application.save()

    oauth2_settings._SCOPES = ['read', 'write', 'users']
    return application


@pytest.fixture
def get_or_create_token(db, api_client, get_application):
    form = {
        'client_id': get_application.client_id,
        'client_secret': get_application.client_secret,
        'grant_type': 'client_credentials'
    }
    response = api_client.post(reverse('oauth2_provider:token'), form)
    return json.loads(response.content.decode("utf-8"))


@pytest.mark.django_db
@pytest.mark.parametrize(
    'username, password, status_code', [
        (None, None, 400),
        (None, 'strong_pass', 400),
        ('user', None, 400),
        ('user', 'invalid_pass', 400),
        ('test', 'strong-test-pass', 200),
    ]
)
def test_login_data_validation(username, password, status_code, api_client, get_or_create_token):
    url = reverse('login')
    data = {
        "login": username,
        "password": password
    }
    token = get_or_create_token
    auth_headers = {
        "HTTP_AUTHORIZATION": token['token_type'] + ' ' + token['access_token'],
        "Accept": 'application/json',
        "Content-Type": 'application/json'
    }
    response = api_client.post(url, data=data, format='json', headers=auth_headers)
    # pretty_print_response(response)

    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, nit, count', [
        (None, None, 0),
        (None, '123456', 0),
        ('Company', None, 0),
        ('Empresa Test', '123456789', 1),
    ]
)
def test_profile_create(name, nit, count, create_user):
    # with pytest.raises(IntegrityError) as e:
    try:
        com = Company()
        com.name = name
        com.nit = nit
        com.description = 'Empresa Test'
        com.contact_name = 'Contacto test'
        com.contact_email = 'test@abc.com'
        com.contact_phone = '1234567'
        filename = str(settings.ROOT_DIR)+'\\account\\test.jpg'
        with open(filename, 'rb') as doc_file:
            com.logo.save('test.jpg', File(doc_file), save=True)

        com.save()
        rol = Rol()
        rol.name = 'Test'
        rol.code = '10'
        rol.save()

        profile = Profile()
        profile.user = create_user(username='test', email='test@test.com', first_name='Tester')
        profile.rol = rol
        profile.phone = '3115556667'
        profile.company = com
        profile.save()

        assert Company.objects.count() == count
        assert Rol.objects.count() == count
        assert Profile.objects.count() == count
        # assert str(profile) == 'Tester (' + str(rol) + ')'
    except IntegrityError as e:
        assert 'null' in str(e)


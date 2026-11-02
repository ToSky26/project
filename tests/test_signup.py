from http import HTTPStatus

import pytest


class TestAuthSignup:
    """Тесты для проверки регистрации пользователя."""
    def test_signup_success(self, session, base_url, fake):
        email = fake.unique.email()
        signup_data = {'email': email, 'lang': 'en', 'utm': ''}
        response = session.post(
            f'{base_url}/api/Auth/signup',
            json=signup_data,
            timeout=10,
        )
        assert response.status_code == HTTPStatus.OK, (
            'Ожидался успешный ответ со статусом 200'
        )

        response_data = response.json()
        assert response_data['email'] == email
        assert response_data['lang'] == 'en'
        assert response_data['token'], 'Токен не должен быть пустым'

    @pytest.mark.parametrize(
        'email, expected_code, expected_message',
        [
            (
                'invalid-email',
                'user.email.isInvalid',
                'Invalid email format',
            ),
            (
                '',
                'user.email.isRequired',
                'Email is required.',
            ),
        ],
    )
    def test_signup_email_validation(
        self,
        session,
        base_url,
        email,
        expected_code,
        expected_message
    ):
        signup_data = {'email': email, 'lang': 'en'}
        response = session.post(
            f'{base_url}/api/Auth/signup',
            json=signup_data,
            timeout=10,
        )
        assert response.status_code == HTTPStatus.CONFLICT, (
            'Ожидался статус 409 при ошибке валидации'
        )

        response_data = response.json()
        assert response_data['error']['code'] == expected_code
        assert response_data['error']['message'] == expected_message
        assert response_data['error']['values'] == email

    def test_signup_with_invalid_json(self, session, base_url):
        invalid_json = '{"email": "test@example.com",}'
        response = session.post(
            f'{base_url}/api/Auth/signup',
            data=invalid_json,
            headers={'Content-Type': 'application/json'},
            timeout=10,
        )
        assert response.status_code == HTTPStatus.CONFLICT, (
            'Ожидался статус 409 при отправке некорректного JSON'
        )

        response_data = response.json()
        assert response_data['error']['code'] == 'validation.failed'
        assert response_data['error']['values'] == 'validation failed'

    def test_signup_with_same_email_twice(self, session, base_url, fake):
        email = fake.unique.email()
        signup_data = {'email': email, 'lang': 'en', 'utm': '', }

        first_response = session.post(
            f'{base_url}/api/Auth/signup',
            json=signup_data,
            timeout=10,
        )
        second_response = session.post(
            f'{base_url}/api/Auth/signup',
            json=signup_data,
            timeout=10,
        )
        assert first_response.status_code == HTTPStatus.OK, (
            'Первая регистрация должна завершиться успешно'
        )

        first_response_data = first_response.json()

        assert first_response_data['email'] == email
        assert first_response_data['lang'] == 'en'
        assert first_response_data['token']
        assert second_response.status_code == HTTPStatus.TOO_MANY_REQUESTS, (
            'Ожидался статус 429 при повторной отправке запроса'
        )

        second_response_data = second_response.json()

        assert second_response_data['error']['code'] == (
            'user.signup.resetTokenSent'
        )
        assert second_response_data['error']['message'] == (
            'A password reset email has already been sent. '
            'Please check your email (including spam folder).'
        )
        assert second_response_data['error']['values']['email'] == email

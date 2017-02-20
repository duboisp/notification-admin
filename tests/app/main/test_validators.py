import pytest
from app.main.forms import RegisterUserForm, ServiceSmsSender
from app.main.validators import ValidGovEmail, NoCommasInPlaceHolders, OnlyGSMCharacters
from wtforms import ValidationError
from unittest.mock import Mock


@pytest.mark.parametrize('password', [
    'govuknotify', '11111111', 'kittykat', 'evangeli'
])
def test_should_raise_validation_error_for_password(
    client,
    mock_get_user_by_email,
    password,
):
    form = RegisterUserForm()
    form.name.data = 'test'
    form.email_address.data = 'teset@example.gov.uk'
    form.mobile_number.data = '441231231231'
    form.password.data = password

    form.validate()
    assert 'Choose a password that’s harder to guess' in form.errors['password']


def test_valid_email_not_in_valid_domains(
    client
):
    form = RegisterUserForm(email_address="test@test.com", mobile_number='441231231231')
    assert not form.validate()
    assert "Enter a central government email address" in form.errors['email_address'][0]


def test_valid_email_in_valid_domains(
    client
):
    form = RegisterUserForm(
        name="test",
        email_address="test@my.gov.uk",
        mobile_number='4407888999111',
        password='an uncommon password')
    form.validate()
    assert form.errors == {}


def test_invalid_email_address_error_message(
    client
):
    form = RegisterUserForm(
        name="test",
        email_address="test.com",
        mobile_number='4407888999111',
        password='1234567890')
    assert not form.validate()

    form = RegisterUserForm(
        name="test",
        email_address="test.com",
        mobile_number='4407888999111',
        password='1234567890')
    assert not form.validate()


def _gen_mock_field(x):
    return Mock(data=x)


@pytest.mark.parametrize("email", [
    'test@gov.uk',
    'test@GOV.UK',
    'test@gov.uK',
    'test@test.test.gov.uk',
    'test@test.gov.uk',
    'test@mod.uk',
    'test@ddc-mod.org',
    'test@test.ddc-mod.org',
    'test@gov.scot',
    'test@test.gov.scot',
    'test@parliament.uk',
    'test@gov.parliament.uk',
    'test@nhs.uk',
    'test@gov.nhs.uk',
    'test@nhs.net',
    'test@gov.nhs.net',
    'test@police.uk',
    'test@gov.police.uk',
    'test@GOV.PoliCe.uk',
    'test@ucds.email',
    'test@naturalengland.org.uk',
    'test@hmcts.net',
])
def test_valid_list_of_white_list_email_domains(
    client,
    email,
):
    email_domain_validators = ValidGovEmail()
    email_domain_validators(None, _gen_mock_field(email))


@pytest.mark.parametrize("email", [
    'test@ukgov.uk',
    'test@gov.uk.uk',
    'test@gov.test.uk',
    'test@ukmod.uk',
    'test@mod.uk.uk',
    'test@mod.test.uk',
    'test@ukddc-mod.org',
    'test@ddc-mod.org.uk',
    'test@ddc-mod.uk.org',
    'test@ukgov.scot',
    'test@gov.scot.uk',
    'test@gov.test.scot',
    'test@ukparliament.uk',
    'test@parliament.uk.uk',
    'test@parliament.test.uk',
    'test@uknhs.uk',
    'test@nhs.uk.uk',
    'test@uknhs.net',
    'test@nhs.net.uk',
    'test@nhs.test.net',
    'test@ukpolice.uk',
    'test@police.uk.uk',
    'test@police.test.uk',
    'test@ucds.com'
])
def test_invalid_list_of_white_list_email_domains(
    client,
    email,
):
    email_domain_validators = ValidGovEmail()
    with pytest.raises(ValidationError):
        email_domain_validators(None, _gen_mock_field(email))


def test_for_commas_in_placeholders(
    client
):
    with pytest.raises(ValidationError) as error:
        NoCommasInPlaceHolders()(None, _gen_mock_field('Hello ((name,date))'))
    assert str(error.value) == 'You can’t have commas in your fields'
    NoCommasInPlaceHolders()(None, _gen_mock_field('Hello ((name))'))


@pytest.mark.parametrize('msg', ['The quick brown fox', 'Thé “quick” bröwn fox\u200B'])
def test_gsm_character_validation(client, msg):
    OnlyGSMCharacters()(None, _gen_mock_field(msg))


@pytest.mark.parametrize('data, err_msg', [
    (
        '∆ abc 📲 def 📵 ghi',
        (
            'You can’t use ∆, 📲 or 📵 in text messages. '
            'They won’t show up properly on everyone’s phones.'
        )
    ),
    (
        '📵',
        (
            'You can’t use 📵 in text messages. '
            'It won’t show up properly on everyone’s phones.'
        )
    ),
])
def test_non_gsm_character_validation(data, err_msg, client):
    with pytest.raises(ValidationError) as error:
        OnlyGSMCharacters()(None, _gen_mock_field(data))

    assert str(error.value) == err_msg


def test_sms_sender_form_validation(
    client,
    mock_get_user_by_email,
):
    form = ServiceSmsSender()

    form.sms_sender.data = 'elevenchars'
    form.validate()
    assert not form.errors

    form.sms_sender.data = ''
    form.validate()
    assert not form.errors

    form.sms_sender.data = 'morethanelevenchars'
    form.validate()
    assert "Enter fewer than 11 characters" == form.errors['sms_sender'][0]

    form.sms_sender.data = '###########'
    form.validate()
    assert 'Use letters and numbers only' == form.errors['sms_sender'][0]

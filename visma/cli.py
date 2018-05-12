import click
import webbrowser
import requests
import datetime
import json

@click.group()
def cli():
    pass


@cli.command()
@click.option('--client', prompt=True, help='Client ID')
@click.option('--browser', default='chrome', help='Specify browser')
@click.option('--production', is_flag=True, )
def request_access(client, browser, production):
    click.echo('Opening webpage')

    __browser = webbrowser.get(browser)

    if production:
        __browser.open((f'https://identity.vismaonline.com/connect/authorize'
                        f'?client_id='
                        f'{client}&redirect_uri=https://identity.vismaonline'
                        f'.com/redirect_receiver&scope=ea:api%20offline_access'
                        f'%20ea:sales%20ea:accounting%20ea:purchase&state=FromPythonCLI&response_type=code'
                        f'&prompt=login'), new=1)
    else:
        __browser.open((f'https://identity-sandbox.test.vismaonline.com'
                        f'/connect/authorize'
                        f'?client_id={client}&'
                        f'redirect_uri=https://identity-sandbox.test'
                        f'.vismaonline.com/redirect_receiver&scope=ea:api%20offline_access'
                        f'%20ea:sales%20ea:accounting%20ea:purchase&state=FromPythonCLI&response_type=code'
                        f'&prompt=login'), new=1)


@cli.command()
@click.option('--code', prompt=True, help='Client ID')
@click.option('--client', prompt=True, help='Client ID')
@click.option('--secret', prompt=True, help='Client ID')
@click.option('--production', is_flag=True, )
def get_token(code, client, secret, production):

    TEST_URL = 'https://identity-sandbox.test.vismaonline.com/connect/token'
    PROD_URL = 'https://identity.vismaonline.com/connect/token'
    credentials = (client, secret)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    data = f'grant_type=authorization_code&code={code}&redirect_uri=https://identity-sandbox.test.vismaonline.com/redirect_receiver'

    if production:
        response = requests.post(PROD_URL, data,  auth=credentials, headers=headers)
    else:
        response = requests.post(TEST_URL, data,  auth=credentials, headers=headers)

    auth_info = response.json()
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    # removes a minute so we dont end up not beeing authenticated because of
    # time difference between client and server.
    expires = now + datetime.timedelta(
        seconds=(auth_info.get('expires_in', 60)-60))
    auth_info['expires'] = expires.isoformat()

    click.echo(
        json.dumps(auth_info)
    )


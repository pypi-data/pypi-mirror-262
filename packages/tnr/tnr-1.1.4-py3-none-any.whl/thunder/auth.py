import click
from thunder import api
from thunder import auth_helper


def login() -> tuple:
    id_token, refresh_token, uid = api.authenticate_user()
    if id_token and refresh_token:
        auth_helper.save_tokens(id_token, refresh_token, uid)
        click.echo("Logged in successfully.")
        return id_token, refresh_token, uid

    else:
        return None, None, None


def logout():
    auth_helper.delete_data()
    click.echo("Logged out successfully.")


def handle_token_refresh(refresh_token: str) -> tuple:
    new_id_token, new_refresh_token, uid = api.refresh_id_token(refresh_token)
    if new_id_token and new_refresh_token:
        auth_helper.save_tokens(new_id_token, new_refresh_token, uid)
        return new_id_token, new_refresh_token, uid
    return None, None, None


def load_tokens() -> tuple:
    credentials_file_path = auth_helper.get_credentials_file_path()
    try:
        with open(credentials_file_path, "r", encoding="utf-8") as file:
            encrypted_id_token = file.readline().strip()
            encrypted_refresh_token = file.readline().strip()
            uid = file.readline().strip()
            if encrypted_id_token and encrypted_refresh_token:
                return (
                    auth_helper.decrypt_data(encrypted_id_token),
                    auth_helper.decrypt_data(encrypted_refresh_token),
                    uid,
                )
            else:
                return None, None, None
    except FileNotFoundError:
        return None, None, None

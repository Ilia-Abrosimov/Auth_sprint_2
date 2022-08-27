import click
from db.db import db
from db.db_models import User
from flask import Blueprint

cli_bp = Blueprint('create', __name__)


@cli_bp.cli.command('superuser')
@click.argument('email')
@click.argument('password')
def create(email, password):
    obj_in = User(
        email=email,
        is_superuser=True
    )
    obj_in.set_password(password)
    db.session.add(obj_in)
    db.session.commit()
    db.session.refresh(obj_in)

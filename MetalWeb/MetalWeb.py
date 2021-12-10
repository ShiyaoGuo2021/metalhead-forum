from MetalWeb import MetalWeb, db
from MetalWeb.models import User


@MetalWeb.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

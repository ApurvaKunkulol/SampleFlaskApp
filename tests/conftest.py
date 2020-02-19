from pytest import fixture


@fixture(scope='module')
def api_client():
    from .. import api_flask_restplus
    api_flask_restplus.app.testing = True
    return api_flask_restplus.app.test_client()

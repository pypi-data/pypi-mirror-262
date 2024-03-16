import os

from webtest import TestApp
from tg.configuration.app_config import AppConfig
from tg import TGController, expose
from tgext.tw2 import plugme


import tw2.forms as tw2f
import tw2.core as tw2c
class TW2MovieForm(tw2f.TableForm):
    title = tw2f.TextField(validator=tw2c.Required)
    year = tw2f.TextField(size=4, validator=tw2c.IntValidator)

tw2_movie_form = TW2MovieForm()


class RootController(TGController):
    @expose('kajiki:kajiki_form.xhtml')
    def tw2form(self):
        return dict(form=tw2_movie_form)


def test_tw2_form_rendering():
    conf = AppConfig(minimal=True, root_controller=RootController())
    conf.prefer_toscawidgets2 = True
    conf.paths['templates'] = [os.path.dirname(__file__)]
    conf.renderers = ['json', 'kajiki']
    conf.default_renderer = 'json'
    plugme(conf._configurator)

    app = conf.make_wsgi_app(full_stack=True)
    app = TestApp(app)

    resp = app.get('/tw2form')
    assert "form" in resp

    for expected_field in ['name="year"', 'name="title"']:
        assert expected_field in resp, resp

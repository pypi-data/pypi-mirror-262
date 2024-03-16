from json import loads

import tw2.core as tw2c
import tw2.forms as tw2f

from webtest import TestApp
import tg
from tg.configuration.app_config import AppConfig
from tg import TGController, expose
from tg.decorators import expose, validate, before_render, before_call, Decoration
from tg.controllers.util import validation_errors_response
from tgext.tw2 import plugme


class MovieForm(tw2f.TableForm):
    title = tw2f.TextField(validator=tw2c.Required)
    year = tw2f.TextField(size=4, validator=tw2c.IntValidator)
movie_form = MovieForm(action='save_movie')


class FormWithFieldSet(tw2f.TableForm):
    class fields1(tw2f.ListFieldSet):
        f1 = tw2f.TextField(validator=tw2c.Required)

    class fields2(tw2f.ListFieldSet):
        f2 = tw2f.TextField(validator=tw2c.IntValidator)


class RootController(TGController):
    @expose()
    def display_form(self, **kwargs):
        return str(myform.render(values=kwargs))

    @expose('json')
    def tw2form_error_handler(self, **kwargs):
        return dict(errors=tg.request.validation.errors)

    @expose('json:')
    @validate(form=movie_form, error_handler=tw2form_error_handler)
    def send_tw2_to_error_handler(self, **kwargs):
        return 'passed validation'

    @expose()
    @validate({'param': tw2c.IntValidator()},
              error_handler=validation_errors_response)
    def tw2_dict_validation(self, **kwargs):
        return 'NO_ERROR'

    @expose('text/plain')
    @validate(form=FormWithFieldSet, error_handler=tw2form_error_handler)
    def tw2_fieldset_submit(self, **kwargs):
        return 'passed validation'



class TestFormValidation:
    def setup_method(self):
        conf = AppConfig(minimal=True, root_controller=RootController())
        conf.prefer_toscawidgets2 = True
        conf.renderers = ['json', 'kajiki']
        conf.default_renderer = 'json'
        plugme(conf._configurator)

        app = conf.make_wsgi_app(full_stack=True)
        self.app = TestApp(app)

    def test_tw2form_validation(self):
        form_values = {'title': 'Razer', 'year': "t007"}
        resp = self.app.post('/send_tw2_to_error_handler', form_values)
        values = loads(resp.body.decode('utf-8'))
        assert "Must be an integer" in values['errors']['year'],\
        'Error message not found: %r' % values['errors']

    def test_tw2dict_validation(self):
        resp = self.app.post('/tw2_dict_validation', {'param': "7"})
        assert 'NO_ERROR' in str(resp.body)

        resp = self.app.post('/tw2_dict_validation', {'param': "hello"}, status=412)
        assert 'Must be an integer' in str(resp.body)

    def test_tw2_fieldset(self):
        form_values = {'fields1:f1': 'Razer', 'fields2:f2': "t007"}
        resp = self.app.post('/tw2_fieldset_submit', form_values)
        values = loads(resp.body.decode('utf-8'))

        assert "Must be an integer" in values['errors'].get('fields2:f2', ''),\
        'Error message not found: %r' % values['errors']

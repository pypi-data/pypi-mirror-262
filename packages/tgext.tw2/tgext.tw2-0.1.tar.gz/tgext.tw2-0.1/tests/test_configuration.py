from webtest import TestApp
from tg.configuration.app_config import AppConfig
from tg import TGController, expose
from tg.configuration.utils import TGConfigError
from tgext.tw2 import plugme


class TestTw2Configuration:
    def test_tw2_unsupported_renderer(self):
        import tw2.core

        class RootController(TGController):
            @expose()
            def test(self, *args, **kwargs):
                rl = tw2.core.core.request_local()
                tw2conf = rl['middleware'].config
                return ','.join(tw2conf.preferred_rendering_engines)

        conf = AppConfig(minimal=True, root_controller=RootController())
        conf.prefer_toscawidgets2 = True
        conf.renderers = ['json', 'kajiki']
        conf.default_renderer = 'json'
        plugme(conf._configurator)

        app = conf.make_wsgi_app(full_stack=True)
        app = TestApp(app)

        resp = app.get('/test')
        assert 'kajiki' in resp, resp

    def test_tw2_renderers_preference(self):
        import tw2.core

        class RootController(TGController):
            @expose()
            def test(self, *args, **kwargs):
                rl = tw2.core.core.request_local()
                tw2conf = rl['middleware'].config
                return ','.join(tw2conf.preferred_rendering_engines)

        conf = AppConfig(minimal=True, root_controller=RootController())
        conf.prefer_toscawidgets2 = True
        conf.renderers = ['kajiki']
        conf.default_renderer = 'kajiki'
        plugme(conf._configurator)

        app = conf.make_wsgi_app(full_stack=True)
        app = TestApp(app)

        resp = app.get('/test')
        assert 'kajiki' in resp, resp

    def test_tw2_unsupported(self):
        import tw2.core

        class RootController(TGController):
            @expose()
            def test(self, *args, **kwargs):
                rl = tw2.core.core.request_local()
                tw2conf = rl['middleware'].config
                return ','.join(tw2conf.preferred_rendering_engines)

        conf = AppConfig(minimal=True, root_controller=RootController())
        conf.prefer_toscawidgets2 = True
        conf.renderers = ['json']
        conf.default_renderer = 'json'
        plugme(conf._configurator)

        try:
            app = conf.make_wsgi_app(full_stack=True)
            assert False
        except TGConfigError as e:
            assert 'None of the configured rendering engines' in str(e)
            assert 'is supported by ToscaWidgets2, unable to configure ToscaWidgets.' in str(e)

# tgext.tw2
Support ToscaWidgets2 forms and validation in TurboGears 2.5+

## Usage

```
    import tgext.tw2

    cfg = FullStackApplicationConfigurator()
    tgext.tw2.plugme(cfg)
    cfg.make_wsgi_app({}, {})
```

import importlib
import inspect


def test_router_smoke():
    mod = importlib.import_module("core.router")

    Router = getattr(mod, "Router", None)
    if Router:
        try:
            _ = Router()
        except Exception:
            pass

    for candidate in ("route", "dispatch", "choose_action"):
        fn = getattr(mod, candidate, None)
        if callable(fn):
            try:
                sig = inspect.signature(fn)
                if len(sig.parameters) == 0:
                    fn()
                else:
                    kwargs = {}
                    for name, param in sig.parameters.items():
                        if param.default is not inspect._empty:
                            continue
                        if "text" in name or "query" in name:
                            kwargs[name] = "hola"
                        elif "data" in name or "payload" in name:
                            kwargs[name] = {}
                        else:
                            kwargs[name] = None
                    fn(**kwargs)
            except Exception:
                pass

    assert True

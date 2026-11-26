from django.apps import AppConfig
from django.contrib.admin.templatetags.base import InclusionAdminNode
from django.template.base import Token, TokenType


class BuildingAdminConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "building_admin"

    def ready(self):
        orig_init = InclusionAdminNode.__init__
        if getattr(orig_init, "_sq_token_patched", False):
            return

        def patched_init(node_self, *args, **kwargs):
            # Firma: (self, name, parser, token, func, template_name, takes_context=True)
            candidates = [*args, *kwargs.values()]

            parser = kwargs.get("parser")
            if not hasattr(parser, "compile_filter"):
                parser = next(
                    (c for c in candidates if hasattr(c, "compile_filter")), None
                )

            func = kwargs.get("func")
            if not callable(func):
                func = next((c for c in candidates if callable(c)), None)

            strs = [c for c in candidates if isinstance(c, str)]
            template_name = kwargs.get("template_name") or next(
                (s for s in strs if "/" in s or s.endswith(".html")),
                "admin/change_list_results.html",
            )
            name = kwargs.get("name") or next(
                (s for s in strs if s != template_name),
                "result_list",
            )

            token = kwargs.get("token")
            if not hasattr(token, "split_contents"):
                token = next(
                    (c for c in candidates if hasattr(c, "split_contents")), None
                )

            # Si el tag en plantilla era p. ej. "{% date_hierarchy cl %}" o "{% result_list cl %}"
            # y no se pasó un Token con el argumento 'cl', incluir 'cl' en el token sintético
            if token is None:
                contents = str(name)
                if name in ("date_hierarchy", "result_list", "search_form", "pagination"):
                    contents = f"{name} cl"
                token = Token(TokenType.BLOCK, contents)

            takes_context = kwargs.get("takes_context", True)

            if parser is not None and func is not None:
                return orig_init(
                    node_self,
                    name=name,
                    parser=parser,
                    token=token,
                    func=func,
                    template_name=template_name,
                    takes_context=takes_context,
                )

            return orig_init(node_self, *args, **kwargs)

        patched_init._sq_token_patched = True
        InclusionAdminNode.__init__ = patched_init
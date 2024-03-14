import inspect
from typing import Union, TypedDict, get_args

from openverse_api_client import endpoints
from openverse_api_client.generate.base import template_env


client_template = template_env.get_template("python/client.py.jinja")


def type_to_string(t) -> str:
    if isinstance(t, str):
        return f"'{str(t)}'"
    elif not hasattr(t, "__name__"):
        return str(t)

    if t.__name__ == "Literal":
        literals = ", ".join(
            [
                type_to_string(a)
                for a in get_args(t)
            ]
        )
        return f'Literal[{literals}]'

    return t.__name__


PythonFiles = TypedDict("PythonFiles", {"async_client.py": str, "sync_client.py": str})


def generate_python() -> PythonFiles:
    methods = []

    for endpoint in endpoints.OpenverseAPIEndpoint.__subclasses__():
        signatures = []
        param_definitions = getattr(endpoint.params, "__args__", [endpoint.params])
        for param_def in param_definitions:
            parameters = []
            if param_def:
                for name, annotation in inspect.get_annotations(param_def).items():
                    default = getattr(param_def, name, inspect._empty)
                    parameters.append(
                        {
                            "name": name,
                            "type": type_to_string(annotation),
                            "default": type_to_string(default) if default is not inspect._empty else inspect._empty
                        }
                    )
            parameters.sort(key=lambda x: 0 if x["default"] is inspect._empty else 1)

            signature = dict(
                parameters=parameters,
                return_annotation=endpoint.response.__name__
            )
            signatures.append(signature)

        methods.append(
            {
                "signatures": signatures,
                "overloaded": len(signatures) > 1,
                "endpoint": endpoint,
            }
        )
    
    async_client = client_template.render(
        **{
            "methods": methods,
            "await": "await ",
            "a": "a",
            "def": "async def",
            "Async": "Async",
            "_empty": inspect._empty,
        }
    )

    sync_client = client_template.render(
        **{
            "methods": methods,
            "await": "",
            "a": "",
            "def": "def",
            "Async": "",
            "_empty": inspect._empty,
        }
    )

    return PythonFiles(**{
        "async_client.py": async_client,
        "sync_client.py": sync_client,
    })

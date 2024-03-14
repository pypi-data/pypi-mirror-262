from jinja2 import Environment, PackageLoader, select_autoescape


template_env = Environment(
    loader=PackageLoader("openverse_api_client"),
    autoescape=select_autoescape()
)


generated_disclaimer = """
This file 
"""
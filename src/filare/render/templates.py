from pathlib import Path

import jinja2


def get_template(template_name, extension=""):
    """Load a Jinja2 template from the bundled templates directory."""
    templates_root = Path(__file__).resolve().parent.parent / "templates"
    template_file_path = jinja2.FileSystemLoader(templates_root)
    jinja_env = jinja2.Environment(
        loader=template_file_path, undefined=jinja2.StrictUndefined
    )

    return jinja_env.get_template(template_name + extension)

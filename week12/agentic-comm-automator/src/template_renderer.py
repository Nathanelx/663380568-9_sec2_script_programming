# agentic-comm-automator/src/template_renderer.py
import string

from .utils import setup_logging

logger = setup_logging(__name__)


class TemplateRenderer:
    """
    A simple template renderer using Python's str.format syntax:
    "{report_date}", "{sales_figure:.2f}", "{attachments_meta[0][filepath]}".
    """
    def __init__(self):
        self._formatter = string.Formatter()

    def render(self, template_string, context):
        """
        Renders a template string using a dictionary context.
        Raises ValueError if a placeholder is missing from the context.
        """
        if template_string is None:
            return ""
        try:
            return self._formatter.vformat(template_string, [], context)
        except (KeyError, IndexError) as e:
            logger.error(f"Missing key in template context: {e}. Template: '{template_string}' "
                         f"Context keys: {list(context.keys())}")
            raise ValueError(f"Missing context key: {e}")
        except Exception as e:
            logger.error(f"Error rendering template: {e}. Template: '{template_string}'")
            raise

import re
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django import template

register = template.Library()

@register.filter
def render_codeblocks(value):
    """
    Replace Markdown-style code blocks (triple backticks) with HTML <pre><code> blocks.
    Escapes HTML tags inside the code block and converts newlines to <br> for line breaks.
    """
    def replace_codeblock(match):
        code_content = match.group(1)  # Get the content inside the triple backticks
        
        # Replace newlines with <br> for rendering line breaks
        formatted_content = code_content.replace("\n", "<br>")
        return f'<pre><code>{formatted_content}</code></pre>'
    
    # Escape HTML tags outside the code blocks first
    value = escape(value)

    # Use regex to find and replace triple backticks with <pre><code> blocks
    formatted_value = re.sub(
        r'```(.*?)```',  # Match content between triple backticks
        replace_codeblock,  # Apply the escaping and formatting function
        value,
        flags=re.DOTALL  # Match across multiple lines
    )
    

    # Mark the final string as safe to render HTML in the template
    return mark_safe(formatted_value)

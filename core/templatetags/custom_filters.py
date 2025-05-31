import re
import markdown
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
    value = re.sub(
        r'```(.*?)```',  # Match content between triple backticks
        replace_codeblock,  # Apply the escaping and formatting function
        value,
        flags=re.DOTALL  # Match across multiple lines
    )

    # Handle ## headings → <h2>
    value = re.sub(
        r'^## (.+)$',
        r'<h2>\1</h2>',
        value,
        flags=re.MULTILINE
    )

    # Handle bold **text** → <strong>
    value = re.sub(
        r'\*\*(.+?)\*\*',
        r'<strong>\1</strong>',
        value
    )

    # Handle italic *text* → <em>
    value = re.sub(
        r'\*(.+?)\*',
        r'<em>\1</em>',
        value
    )

    # Handle horizontal rule --- → <hr>
    value = re.sub(
        r'^---$',
        r'<hr>',
        value,
        flags=re.MULTILINE
    )
    

    # Mark the final string as safe to render HTML in the template
    return mark_safe(value)

@register.filter
def render_markdown(value):
    """
    Render full Markdown content, including code blocks, headings, bold, etc.
    """
    html = markdown.markdown(
        value,
        extensions=['fenced_code', 'codehilite']  # fenced_code = ``` blocks, codehilite = syntax highlighting (optional)
    )
    return mark_safe(html)

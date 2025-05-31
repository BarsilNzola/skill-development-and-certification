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

    # Headings
    value = re.sub(
        r'\s*### (.+)', 
        r'<h3>\1</h3>', 
        value
    )

    value = re.sub(
        r'\s*## (.+)', 
        r'<h2>\1</h2>', 
        value
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

    # Horizontal rule
    value = re.sub(
        r'\n?---\n?', 
        r'<hr>', 
        value
    )

    # Handle bullet lists (- item)
    def replace_bullets(text):
        lines = text.split('\n')
        result = []
        in_list = False

        for line in lines:
            if re.match(r'^- (.+)', line):
                if not in_list:
                    result.append('<ul>')
                    in_list = True
                item = re.sub(r'^- (.+)', r'<li>\1</li>', line)
                result.append(item)
            else:
                if in_list:
                    result.append('</ul>')
                    in_list = False
                result.append(line)
        
        if in_list:
            result.append('</ul>')

        return '\n'.join(result)
    value = replace_bullets(value)

    # Handle inline links [text](url)
    value = re.sub(
        r'\[(.*?)\]\((.*?)\)', 
        r'<a href="\2" target="_blank">\1</a>', 
        value
    )

    # Handle inline code spans `code`
    value = re.sub(
        r'`([^`]+)`', 
        r'<code>\1</code>', 
        value
    )
    
    # Mark the final string as safe to render HTML in the template
    return mark_safe(value)


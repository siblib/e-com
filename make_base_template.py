with open('header_part.html', 'r', encoding='utf-8') as f:
    header = f.read()

with open('footer_part.html', 'r', encoding='utf-8') as f:
    footer = f.read()

base_content = header + """
{% block content %}
{% endblock %}
""" + footer

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(base_content)

print("Created base.html successfully.")

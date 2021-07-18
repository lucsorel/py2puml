from py2puml.py2puml import py2puml

# outputs the PlantUML content in the terminal
print(''.join(
    py2puml('py2puml/domain', 'py2puml.domain')
))

# writes the PlantUML content in a file
with open('py2puml/py2puml.domain.puml', 'w') as puml_file:
    puml_file.writelines(py2puml('py2puml/domain', 'py2puml.domain'))

from tests import __version__, __description__

# Ensures the library version is modified in the pyproject.toml file when upgrading it (pull request)
def test_version():
    assert __version__ == '0.7.2'

# Description also output in the CLI
def test_description():
    assert __description__ == 'Generate PlantUML class diagrams to document your Python application.'

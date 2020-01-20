clear && clear
export FLASK_ENV=testing
pytest --cov=blueprints --cov-report html -s
export FLASK_ENV=development

# --cov-fail-under=80 
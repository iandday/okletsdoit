# Set the default shell for commands
set shell := ["bash", "-c"]


#----Setup Commands----#
setup:
    @echo "Installing npm dependencies"
    npm install
    @echo "Installing python depdencies"
    uv sync


#----Development commands----#
css:
    @echo "Building CSS with Tailwind and daisyUI 5"
    npm run build-css

dev:
    @echo "Starting django server"
    uv run --group dev manage.py runserver_plus

makemigrations:
    @echo "Running Django makemigrations..."
    uv run python manage.py makemigrations

# Run migrations
migrate:
    @echo "Running Django migrations..."
    uv run python manage.py migrate


#----Pre-commit commands----#
lint:
    uv run --group dev ruff check .
    uv run --group dev mypy .

test:
    uv run --group dev pytest

pre-commit:
    uv run --group dev pre-commit run --all-files


#----Build commands----#
css-prod:
    @echo "Building production CSS"
    npm run build-css-prod

collectstatic:
    @echo "Collecting static files..."
    uv run python manage.py collectstatic --noinput

superuser:
    @echo "Creating a Django superuser..."
    python manage.py createsuperuser --no-input





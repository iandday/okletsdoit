# Set the default shell for commands
set shell := ["bash", "-c"]


# setup
setup:
    @echo "Installing npm dependencies"
    npm install
    @echo "Installing python depdencies"
    uv sync

# Build CSS with daisyUI 5
css:
    @echo "Building CSS with Tailwind and daisyUI 5"
    npm run build-css

# Build CSS for production
css-prod:
    @echo "Building production CSS"
    npm run build-css-prod

# Standard development server
dev:
    @echo "Starting django server"
    uv run --group dev manage.py runserver_plus



# Run linting
lint:
    uv run --group dev ruff check .
    uv run --group dev mypy .

# Run tests
test:
    uv run --group dev pytest

# Run pre-commit hooks
pre-commit:
    uv run --group dev pre-commit run --all-files

# Make migrations
makemigrations:
    @echo "Running Django makemigrations..."
    uv run python manage.py makemigrations

# Run migrations
migrate:
    @echo "Running Django migrations..."
    uv run python manage.py migrate

# Collect static files
collectstatic:
    @echo "Collecting static files..."
    uv run python manage.py collectstatic --noinput
#------



# Build the Docker image
docker-build:
    @echo "Building the Docker image..."
    docker build -t box_buddy .

# Run the Docker container
docker-run:
    @echo "Running the Docker container..."
    docker run --rm -it -p 8000:8000 box_buddy



# Create a superuser
superuser:
    @echo "Creating a Django superuser..."
    python manage.py createsuperuser



# Clean up Docker containers and images
docker-clean:
    @echo "Cleaning up Docker containers and images..."
    docker system prune -af

# Install dependencies
install:
    @echo "Installing dependencies..."
    pip install -r requirements.txt

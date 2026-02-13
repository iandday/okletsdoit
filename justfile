# Set the default shell for commands

set shell := ["bash", "-c"]

# ----Setup Commands----#
setup:
    @echo "Installing python depdencies"
    uv sync

# ----Development commands----#
up:
    @echo "Starting the development environment"
    docker compose -f docker/docker-compose.yml build && docker compose -f docker/docker-compose.yml up

makemigrations:
    @echo "Running Django makemigrations..."
    uv run python app/manage.py makemigrations

# Run migrations
migrate:
    @echo "Running Django migrations..."
    uv run python app/manage.py migrate

docs:
    uv run --all-groups mkdocs serve

# ----Pre-commit commands----#
lint:
    uv run --group dev ruff check backend
    cd backend && uv run --group dev mypy .

test:
    uv run --group dev pytest

pre-commit:
    uv run --group dev pre-commit run --all-files

local-scan:
    @echo "Scanning local Docker image for vulnerabilities..."
    docker build -f docker/Dockerfile --target production -t okletsdoit:test .
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
        -v "$(pwd)/.trivyignore.yaml:/work/.trivyignore.yaml" \
        -w /work \
        aquasec/trivy image okletsdoit:test --ignore-unfixed \
        --vuln-type os,library --severity CRITICAL,HIGH

#----Build commands----#

collectstatic:
    @echo "Collecting static files..."
    uv run python manage.py collectstatic --noinput

superuser:
    @echo "Creating a Django superuser..."
    python manage.py createsuperuser --no-input

# ----Production commands----#
build:
    @echo "Building production Docker image (multi-stage)"
    DOCKER_BUILDKIT=1 docker build \
        --file docker/Dockerfile \
        --target runtime \
        --build-arg BUILDKIT_INLINE_CACHE=1 \
        -t okletsdoit:latest .

# Check image size
image-size:
    @echo "Checking image sizes..."
    docker images okletsdoit:latest

# Scan for vulnerabilities
scan-image:
    @echo "Scanning image for vulnerabilities..."
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
        aquasec/trivy image okletsdoit:latest

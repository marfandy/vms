init-app:
	@echo "Installing dependencies..."
	@pip install -r requirements.txt
	@echo "Applying database migrations..."
	@python manage.py migrate


test:
	@python manage.py test $(testr)


run:
	@python manage.py runserver
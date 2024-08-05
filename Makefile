.PHONY: install
install:
	@echo "Installing packages..."
	@pip install .
	@echo "Done."

.PHONY: install-dev
install-dev:
	@echo "Installing dev packages..."
	@pip install pipx
	@pipx install pdm
	@pdm install --dev
	@echo "Installing pre-commit hooks..."
	@pre-commit install

.PHONY: check-hooks
check-hooks:
	@echo "Checking pre-commit hooks..."
	@pre-commit run --all-files
	@echo "Done."

.PHONY: init-migrations
init-migrations:
	@flask --app 'cor_iesu.app:create_app("./config/dev-config.ini")' db init

.PHONY: migrations
migrations:
	@flask --app 'cor_iesu.app:create_app("./config/dev-config.ini")' db migrate -m "Migration at $(date)"
	@flask --app 'cor_iesu.app:create_app("./config/dev-config.ini")' db upgrade

.PHONY: run-dev
run-dev:
	@flask --app 'cor_iesu.app:create_app("./config/dev-config.ini")' run

admin:
	python3 src/manage.py createsuperuser --email admin@admin.ru --password 1234 || true

policy:
	python3 src/manage.py create-default-policy || true

alembic-migrate:
	alembic upgrade head

grpc-generate:
	python -m grpc_tools.protoc --python_out=./grpc_package/src/grpc_auth_service/ --pyi_out=./grpc_package/src/grpc_auth_service/ --grpc_python_out=./grpc_package/src/grpc_auth_service/ --proto_path=./protobuf ./protobuf/*.proto

grpc-publish:
	cd grpc_package && python3 -m build && python3 -m twine upload dist/* --verbose  # Need (my) credentials in .pypirc or share

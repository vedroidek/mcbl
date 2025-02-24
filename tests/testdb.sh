docker run -d \
--name test-db \
-p 5433:5432 \
-e POSTGRES_DB=test_db \
-e POSTGRES_USER=test_user \
-e POSTGRES_PASSWORD=test_password \
--restart on-failure \
--memory 128Mb \
postgres:16.1-alpine3.19
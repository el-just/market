install docker, docker-compose, yandex-cli
    ./install.sh

configure yc
    yc init
    yc container registry configure-docker

run docker-compose
    docker-compose up -d

create db schema
    docker exec -ti veggies_backend_1 alembic upgrade head

init db and add superuser
    docker exec -ti veggies_backend_1 python db_init.py 71234567890 password

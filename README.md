Code for [Airflow Tutorial](https://startdataengineering/post/airflow-tutorial/#dags-can-be-scheduled-or-set-to-run-when-a-dataset-is-updated)

## Setup 

**Prerequisites**

1. [Docker version >= 20.10.17](https://docs.docker.com/engine/install/) and [Docker compose v2 version >= v2.10.2](https://docs.docker.com/compose/#compose-v2-and-the-new-docker-compose-command).

Clone and start the container as shown below: 

```bash
git clone https://github.com/josephmachado/airlfow-tutorial.git
cd airflow-tutorial
docker compose up -d --build
```

Open Airflow at [http://localhost:8080](http://localhost:8080) and stop containers after you are done with `docker compose down`.


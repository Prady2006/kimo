# Courses Backend Api
## Setup | Build


![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)

```sh
 git clone <repo_name>
 cd <repo_name>
 docker compose -f docker-compose.yaml up -d
```

 ✨ Containers for both server and db should be up and running by now . ✨

## Startup Scripts 
Run these commands to populate data in the mongodb .
```sh
 docker exec -it fastapi bash
 node scripts/upload_data.js
 exit
```

> Note : When containers are killed data wont be persisted on to the disk , if you wish to persist the data onto disk , so that on containers restart data is not lost .Kindly add the below command to the docker-compose.yaml .
>
    volumes:
        - type: volume
          source: mongodb_data_volume
          target: /data/db
    volumes:
      mongodb_data_volume:
        external: true


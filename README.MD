# Courses Backend Api
## Setup | Build


![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)

```sh
 git clone <repo_name>
 cd <repo_name>
 docker compose -f docker-compose.yaml up -d
```

 ✨ Containers for both server and db should be up and running by now . ✨
    Server will be running on http://localhost:8000/
## Startup Scripts 
Run these commands to populate data in the mongodb .
```sh
 docker exec -it fastapi bash
 cd scripts && npm install
 cd ..
 node scripts/upload_data.js
 exit
```
Mongo collections and schemas are built by upload_data.js under scripts/ folder, it also creates appropriate compound idx's needed by the search courses, chapters api .
The given script is responsible to parse data from courses.json file and dump onto mongodb .
> Note : When containers are killed data wont be persisted on to the disk , if you wish to persist the data onto disk , so that on containers restart data is not lost .Kindly add the below command to the docker-compose.yaml .
>
    volumes:
        - type: volume
          source: mongodb_data_volume
          target: /data/db
    volumes:
      mongodb_data_volume:
        external: true

# GET /courses
    Query Parameters:
     domains: optional(  partial filter "," seperated mongo object ids )
     title : optional (for sort by  title of course value can only be 1 )
     date : optional (for sort by  date of course value can only be -1 )
     course_rating : optional (for sort by  rating of course value can only be -1) 
     page: optional (for pagination default value is 0 , only accepts integers 0...n )
    
# GET /courses/{course_id}

    Get all the data of a course with course id as course_id . 
    
# GET /chapters/{chapter_id}

    Get all the data of a chapter with chapter id as chapter_id. 
    
# POST /courses/{course_id}/chapters/{chapter_id}

    Body: 
     like : true (Optional)
     dislike: true (Optional)
     Can only send single value at a time either like or dislike set to true .
     
> All the ids mentioned are mongodb object ids .
>

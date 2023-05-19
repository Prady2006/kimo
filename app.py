from fastapi import FastAPI
from pymongo import ASCENDING, DESCENDING
from bson import ObjectId,json_util
from pydantic import BaseModel
import json 
from typing import Union
from config.app_settings import app_settings
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from config.mongo_settings import db

app= FastAPI()

class ChapterUpdate(BaseModel):
    like: bool  = False
    dislike: bool  = False 

@app.get('/courses')
def all_courses(title: Union[int,None] = None , date: Union[int,None]= None, course_rating: Union[int,None]=None, domains: Union[str,None]=None):
    query = {}
    valid_domains = []
    coll = db.get_collection("courses")

    # need to add empty object to satisfy prefix of compound idx .
    if domains is not None: 
        domains = domains.split(",")
        valid_domains = [ObjectId(domain) for domain in domains]
        query["domains"]["$in"] = valid_domains # [ObjectId('hexid'), ....  ]
    
    if title != None and title == 1 : 
        res = []
        cur = coll.find(query,{"chapters":0,"total_like":0,"total_dislike":0}).sort("name",ASCENDING)
        for doc in cur:
            res.append(doc)
        data = json.loads(json_util.dumps(res))
        return {"success": "true", "msg":"Data Found", "data": data}

    
    if date != None and date == -1 : 
        res = []
        cur =   coll.find(query,{"chapters":0,"total_like":0,"total_dislike":0}).sort("date",DESCENDING)
        for doc in cur:
            res.append(doc)
        data = json.loads(json_util.dumps(res))
        return {"success": "true", "msg":"Data Found", "data": data}

    
    if course_rating != None and course_rating == -1:
        res = []
        query=[]
        if len(valid_domains) != 0 : 
            query.append({"$match":{"$in":valid_domains}})
        query.append(
        {
            '$addFields': {
                'rating': {
                    '$cond': {
                        'if': {
                        '$eq': [
                            {
                                '$sum': [
                                    '$total_like', '$total_dislike'
                                ]
                            }, 0
                        ]
                    }, 
                        'then': 0, 
                        'else': {
                        '$divide': [
                            '$total_like', {
                                '$sum': [
                                    '$total_dislike', '$total_like'
                                ]
                            }
                        ]
                    }
                }
            }
        }
        })
        query.append({"$sort":{"rating":-1}})
        query.append({"$project":{"chapters":0,"total_like":0,"total_dislike":0}})
        cur =   coll.aggregate(query)
        for doc in cur:
            res.append(doc)
        data = json.loads(json_util.dumps(res))
        return {"success": "true", "msg":"Data Found", "data": data}



    return {"success": "false" , "msg":"Please provide appropriate sort order ."}
    

@app.get("/courses/{course_id}")
def get_course(course_id: str):
    coll= db.get_collection("courses")
    cur = coll.find_one({"_id": ObjectId(course_id)})
    data = json.loads(json_util.dumps(cur))

    return {"success": "true", "msg": "Data Found", "data": data}

@app.get("/chapters/{chapter_id}")
def get_chapter(chapter_id: str):
    res={}
    coll = db.get_collection("courses")
    cur = coll.find_one({"chapters._id": ObjectId(chapter_id)})

    for chapter in cur["chapters"]:
        if chapter["_id"] == ObjectId(chapter_id):
            res = chapter

    data = json.loads(json_util.dumps(res))
    return {"success": "true", "msg": "Data Found", "data": data}
    

@app.post("/courses/{course_id}/chapters/{chapter_id}")
def update_review(course_id: str, chapter_id: str , body: ChapterUpdate):
    coll = db.get_collection("courses")
    # return body
    if body.like is False and body.dislike is False: 
        return {"success": "false", "msg": "Min. single field required i.e[like,dislike]"}
    
    if body.like is not False:
        coll.find_one_and_update({"_id": ObjectId(course_id)},{"$inc":{
            "chapters.$[elem].like_count": 1,
            "total_like": 1,
            }
            },None, None,False,True,[{"elem._id":ObjectId(chapter_id)}])
        return {"success": "true", "msg":"Data updated"}

    if body.dislike is not False :
        coll.find_one_and_update({"_id": ObjectId(course_id)},{"$inc":{
            "chapters.$[elem].dislike_count": 1, 
            "total_dislike": 1
            }
            },None, None,False,True,[{"elem._id":ObjectId(chapter_id)}])
        return {"success": "true", "msg":"Data updated"}


    

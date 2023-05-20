from fastapi.testclient import TestClient
import app 


client = TestClient(app.app)

def test_all_courses():
    #Testing if data no query parameter is sent.
    response = client.get("/courses")
    print(response)
    assert response.status_code == 200 
    assert response.json() == {"success": "false" , "msg" : "Please provide appropriate sort order ."}

def test_all_courses_with_title_sort():
    #passing invalid params 
    response = client.get("/courses?title=-1")
    assert response.status_code == 200
    assert response.json() == {"success": "false" , "msg":"Please provide appropriate sort order ."}
    response2 = client.get("/courses?title=falskfjlksj")
    assert response2.status_code == 422

def test_all_courses_with_date_sort():
    response = client.get("/courses?date=12")
    assert response.status_code == 200
    assert response.json() == {"success": "false" , "msg":"Please provide appropriate sort order ."}
    response2 = client.get("/courses?date=jkl")
    assert response2.status_code == 422

def test_all_courses_with_rating_sort():
    response =client.get("/courses?course_rating=1")
    assert response.status_code == 200
    assert response.json() == {"success": "false" , "msg":"Please provide appropriate sort order ."}
    
 


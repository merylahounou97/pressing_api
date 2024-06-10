
""" from .test_init import client


def test_token():    
    response = client.post("/token",data={
        "username": "aiounouu@gmail.com",
        "password": "string",
    }, headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    })

    #Vérifier que la requête a fonctionné
    assert response.status_code == 200  """
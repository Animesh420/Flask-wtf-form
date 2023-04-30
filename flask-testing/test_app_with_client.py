import pytest
from app import app

expected = {
        "id": 0,
        "name": "A tale of two cities",
        "author": "Charles dickens",
        "publisher": "Astrabound Publishers",
        "price": 60
    }

new_book = {
        "id": 2,
        "name": "Rich dad poor dad",
        "author": "Robert Kiyosaki",
        "publisher": "Hawkins publishers",
        "price": 87
    }

faulty_book = {
    "publisher": "Daemon publishers",
    "author": "Roman Edward"
}

@pytest.fixture()
def client():
    return app.test_client()


def test_read_with_client(client):
    response = client.get("/get/book/0")
    assert response.status_code == 200
    assert response.get_json() == expected


def test_write_with_client(client):
    response = client.post("/post/book", json=new_book)
    assert response.status_code == 200

def test_write_and_read_with_client(client):
    resp_of_write = client.post("/post/book", json=new_book)
    assert resp_of_write.status_code == 200
    resp_of_read = client.get("/get/book/2")
    assert resp_of_read.status_code == 200
    assert resp_of_read.get_json() == new_book

def test_read_exception_with_client(client):
    response = client.get("/get/book/100")
    assert response.status_code == 404
    assert response.get_json()["message"] == 'There are no books with id: 100'

def test_write_exception_with_client(client):
    response = client.post("/post/book", json=faulty_book)
    assert response.status_code == 404
    assert response.get_json()["message"] == 'The book should have name,author,publisher,price defined, not all found'




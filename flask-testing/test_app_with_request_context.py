from werkzeug.exceptions import HTTPException

import pytest

from app import app, post_book, get_book
from test_app_with_client import new_book, expected, faulty_book


def test_success_write_with_request_context():
    with app.test_request_context("/post/book", method="POST", json=new_book):
        res = post_book()
        assert res == "Book added successfully"


def test_success_read_with_request_contxt():
    with app.test_request_context("/get/book/0", method="GET"):
        res = get_book(0)
        assert res.get_json() == expected


def test_success_read_and_write_with_request_context():
    with app.test_request_context("/post/book", method="POST", json=new_book):
        res = post_book()
        assert res == "Book added successfully"
        res2 = get_book(2)
        assert res2.get_json() == new_book


def test_failure_on_read_with_request_context():
    with app.test_request_context("/get/book/100", method="GET"):
        with pytest.raises(HTTPException) as e:
            res = get_book(100)
        assert e.value.response.get_json()["message"] == 'There are no books with id: 100'


def test_failure_on_write_with_request_context():
    with app.test_request_context("/post/book", method="POST", json=faulty_book):
        with pytest.raises(HTTPException) as e:
            res = post_book()
        assert e.value.response.get_json()[
                   "message"] == 'The book should have name,author,publisher,price defined, not all found'

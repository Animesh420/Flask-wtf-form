from flask import Flask, request, jsonify, abort, make_response
app = Flask(__name__)

books = [{
    "id": 0,
    "name": "A tale of two cities",
    "author": "Charles dickens",
    "publisher": "Astrabound Publishers",
    "price": 60
},
    {
        "id": 1,
        "name": "War and peace",
        "author": "Leo Tolstoy",
        "publisher": "Penguin publisher",
        "price": 45

    }

]


@app.route("/get/book/<int:id_to_query>", methods=["GET"])
def get_book(id_to_query):
    if id_to_query >= len(books):
        msg = "There are no books with id: {}".format(id_to_query)
        abort(make_response(jsonify(message=msg), 404))

    return jsonify(books[id_to_query])


@app.route("/post/book", methods=["POST"])
def post_book():
    new_id = len(books)
    book = request.get_json()

    fields_to_check = ["name", "author", "publisher", "price"]
    if any(f not in book for f in fields_to_check):
        msg = "The book should have {} defined, not all found".format(','.join(fields_to_check))
        abort(make_response(jsonify(message=msg), 404))

    book["id"] = new_id
    books.append(book)
    return "Book added successfully"


if __name__ == '__main__':
    app.run(port=8081)

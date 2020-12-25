from flask import Flask, request, make_response, jsonify
from flask_json_schema import JsonValidationError, JsonSchema
from models import session, insert, delete, User, Post, IntegrityError
from hashlib import md5
from schemas import register_schema, create_post_schema


app = Flask(__name__)
schema = JsonSchema(app)


@app.errorhandler(JsonValidationError)
def validation_error(e):
    body = jsonify({'error': e.message, 'errors': [error.message for error in e.errors]})
    resp = make_response(body, 400)
    return resp


@app.route('/register', methods=['POST'])
@schema.validate(register_schema)
def register():
    data = request.get_json()
    query = insert(User).values(login=data['login'], password=md5(data['password'].encode('utf-8')).hexdigest())
    try:
        session.execute(query)
        session.commit()
    except IntegrityError:
        resp = make_response(f'<h2>User {data["login"]} already exists</h2>', 400)
        resp.headers['Content-Type'] = 'text/plain'
        return resp
    resp = make_response(f'<h2>User {data["login"]} was created successfully</h2>', 200)
    resp.headers['Content-Type'] = 'text/plain'
    return resp


@app.route("/post", methods=['POST'])
@schema.validate(create_post_schema)
def create_post():
    data = request.get_json()
    user = data['user']
    post = data['post']
    id_user = check_user(user['login'], user['password'])
    if id_user == -1:
        return make_response(f'User is not logged in', 401)
    query = insert(Post).values(id_user=id_user, header=post['header'], text=post['text'])
    try:
        session.execute(query)
        session.commit()
    except IntegrityError:
        return make_response('Server error', 500)
    return make_response('Post created!')


@app.route('/post/<int:id_post>', methods=['GET', 'DELETE'])
@schema.validate(register_schema)
def action_post(id_post):
    user = request.get_json()
    id_user = check_user(user['login'], user['password'])
    if id_user == -1:
        return make_response(f'User is not logged in', 401)
    post = session.query(Post).filter(Post.id_post == id_post and Post.id_user == id_user).all()
    if not post:
        return make_response('Post does not exist', 404)
    post = post[0]
    if request.method == 'GET':
        resp = make_response(jsonify(post.get_dict()), 200)
        return resp
    else:
        session.delete(post)
        session.commit()
        return make_response('Post deleted', 200)


def check_user(login, password):
    resp = session.query(User).filter(User.login == login).all()
    if resp and resp[0].password == md5(password.encode('utf-8')).hexdigest():
        return resp[0].id_user
    else:
        return -1


@app.route('/test')
def test():
    return 'hello'


if __name__ == '__main__':
    app.run(debug=True)

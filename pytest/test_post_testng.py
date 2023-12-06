from app import db
from app.auth.model import User
from app.post.model import Post, Category, Tag


def test_create_post(client):
    user = User(username='testing_user', email='testing@example.com', password='test_password')
    db.session.add(user)
    category = Category(name='category')
    db.session.add(category)
    db.session.commit()
    with client:
        client.post('/login3', data={'email': 'testing@example.com', 'password': 'test_password'})
        response = client.post('/post/create', data={
            'title': 'Test Title',
            'text': 'Test Text',
            'type': 'news',
            'category': 1,
            'tags': 'tag1, tag2, tag3'
        })

        assert response.status_code == 302
        post = Post.query.filter_by(title='Test Title').first()
        assert post is not None


def test_create_post_without_auth(client):
    category = Category(name='category')
    db.session.add(category)
    db.session.commit()
    with client:
        response = client.post('/post/create', data={
            'title': 'Test Title',
            'text': 'Test Text',
            'type': 'news',
            'category': 1,
            'tags': 'tag1, tag2, tag3'
        })
        assert response.status_code == 302
        post = Post.query.filter_by(title='Test Title').first()
        assert post is None


def test_list_posts(client):
    add_post()
    with client:
        response = client.get('/post')
        assert b'test title' in response.data


def test_view_post(client):
    add_post()
    with client:
        response = client.get('/post/1')
        assert response.status_code == 200
        assert b'test title' in response.data


def test_update_post(client):
    add_post()
    with client:
        response = client.post('/post/1/update', data={'title': 'Updated title',
                                                       'text': 'Updated text',
                                                       'type': 'other',
                                                       'tags': 'tag4, tag5'})
        assert response.status_code == 302
        updated_post = Post.query.get(1)
        assert updated_post.title == 'Updated title'


def test_delete_post(client):
    add_post()
    with client:
        response = client.post('/post/1/delete')
        assert response.status_code == 302
        deleted_post = Post.query.get(1)
        assert deleted_post is None


def add_post():
    category = Category(name='category')
    db.session.add(category)
    db.session.commit()
    tags = 'tag1, tag2, tag3'
    tags = tags.split(',')
    tags = [tag.strip() for tag in tags if tag]
    new_post = Post(
        title='test title',
        text='test text',
        type='news',
        user_id=1,
        category=category,
        tags=[Tag.get_or_create(tag) for tag in tags]
    )
    db.session.add(new_post)
    db.session.commit()

from flask import Blueprint, render_template, request, redirect, url_for
from .models import Post
from flask import jsonify
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@main.route('/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('create_post.html')

@main.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('edit_post.html', post=post)

@main.route('/delete/<int:post_id>')
def delete_post(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/api/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    posts_list = [{"id": post.id, "title": post.title, "content": post.content} for post in posts]
    return jsonify(posts_list)
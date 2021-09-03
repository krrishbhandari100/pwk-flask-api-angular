from flask import *
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///programmingwithkrrish.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key="""MyR3&|9&#W3pB)/ic5CiF!|9"d*W95o;Z@g6.q'BA.8:;nx>^'b`8N}7E%z<=r'!.jDkrjAFYg/@vr%])W~=;N6."""
db = SQLAlchemy(app)

class Post(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(255), unique=False, nullable=False)
    post_title = db.Column(db.String(255), unique=False, nullable=False)
    post_subtitle = db.Column(db.String(255), unique=False, nullable=False)
    category = db.Column(db.String(255), unique=False, nullable=False)
    post_posted_by = db.Column(db.String(255), unique=False, nullable=False)
    post_desc = db.Column(db.Text, unique=False, nullable=False)
    stime = db.Column(db.String(255), unique=False, nullable=True)

class Video(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(255), unique=False, nullable=False)
    image = db.Column(db.String(255), unique=False, nullable=False)
    video_title = db.Column(db.String(255), unique=False, nullable=False)
    video_subtitle = db.Column(db.String(255), unique=False, nullable=False)
    category = db.Column(db.String(255), unique=False, nullable=False)
    video_posted_by = db.Column(db.String(255), unique=False, nullable=False)
    video_desc = db.Column(db.Text, unique=False, nullable=False)
    stime = db.Column(db.String(255), unique=False, nullable=True)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True, nullable=True)
    first_name = db.Column(db.String(255), unique=False, nullable=True)
    last_name = db.Column(db.String(255), unique=False, nullable=True)
    email = db.Column(db.String(255), unique=False, nullable=True)
    phone_number = db.Column(db.String(255), unique=False, nullable=True)
    desc = db.Column(db.Text, unique=False, nullable=True)


# Api routes
@app.route('/')
def index():
    return redirect('/posts')

# All posts in json
@app.route('/posts')
def posts():
    postobj = Post.query.all()
    data = []
    for i in postobj:
        mdata = {
            'post_title': i.post_title,
            'category': i.category,
            'post_subtitle': i.post_subtitle,
            'post_desc': i.post_desc,
            'slug': i.slug,
            'sno': i.sno,
        }
        pdata = data.append(mdata)
    return jsonify(data)

# posts fetching by the slug
@app.route('/posts/<string:slug>')
def post(slug):
    post = Post.query.filter_by(slug=slug).first()
    post_data = [{
        'post_title': post.post_title,
        'category': post.category,
        'post_subtitle': post.post_subtitle,
        'slug': post.slug,
        'post_posted_by': post.post_posted_by,
        'post_desc': post.post_desc,
        'stime': post.stime,
    }]

    return jsonify(post_data)

# All Videos
@app.route('/videos')
def videos():
    videosobj = Video.query.all()
    data = []
    for i in videosobj:
        mdata = {
            'video_title': i.video_title,
            'video_subtitle': i.video_subtitle,
            'video_desc': i.video_desc,
            'slug': i.slug,
            'sno': i.sno,
            'image': i.image,
            'category': i.category
        }
        pdata = data.append(mdata)
    return jsonify(data)


# Videos Fetching by slug
@app.route('/videos/<string:slug>')
def video(slug):
    videos = Video.query.filter_by(slug=slug).first()
    video_data = [{
        'video_title': videos.video_title,
        'category': videos.category,
        'video_subtitle': videos.video_subtitle,
        'slug': videos.slug,
        'video_posted_by': videos.video_posted_by,
        'video_desc': videos.video_desc,
        'stime': videos.stime,
        'image': videos.image,
    }]

    return jsonify(video_data)

@app.route('/postcategory/<string:category>')
def postcategory(category):
    post = Post.query.filter_by(category=category).all()
    # print(post)
    data = []
    for i in post:
        mdata = {
            'post_title': i.post_title,
            'post_subtitle': i.post_subtitle,
            'post_desc': i.post_desc,
            'slug': i.slug,
            'sno': i.sno,
            'category': i.category
        }
        pdata = data.append(mdata)
    
    return jsonify(data)

@app.route('/videocategory/<string:category>')
def videocategory(category):
    video = Video.query.filter_by(category=category).first()
    video_data = [{
        'video_title': video.video_title,
        'category': video.category,
        'video_subtitle': video.video_subtitle,
        'slug': video.slug,
        'video_posted_by': video.video_posted_by,
        'video_desc': video.video_desc,
        'stime': video.stime,
    }]

    return jsonify(video_data)

# Contact API
@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == 'POST':
        data = request.get_json()
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        phone_number = data['phone_number']
        desc = data['desc']
        contactobj = Contacts(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, desc=desc)
        db.session.add(contactobj)
        db.session.commit()
        return 'We will surely reply on this'
    return 'This is the contacts data'
    

'''---------------------------------------------------------- dashboard endpoints------------------------------------------------------------------'''
@app.route('/admin', methods=["GET", "POST"]) # admin login page
def admin():
    if 'username' in session:
        return redirect('/dashboard')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if(username=='krrish@programmingwithkrrish.com' and password=='0108kb@krrish'):
            session['username'] = username
            return redirect('/dashboard')
        else:
            return 'Incorrect cretentials'
    return render_template('admin.html')

@app.route('/dashboard', methods=["GET", "POST"]) # dashboard page after login
def dashboard():
    if not('username' in session):
        return redirect('/admin')
    return render_template('dashboard.html', postdata=Post.query.all(), videoData=Video.query.all(), contactData=Contacts.query.all())


# Adding endpoints
@app.route('/dashboard/addPost', methods=["GET", "POST"]) # page for adding post in db
def addpost():
    if not('username' in session):
        return redirect('/admin')
    if request.method == 'POST':
        post_title = request.form.get('post_title')
        post_subtitle = request.form.get('post_subtitle')
        post_posted_by = request.form.get('post_posted_by')
        slug = request.form.get('slug')
        desc = request.form.get('desc')
        category = request.form.get('category')
        postobj = Post(post_title=post_title, slug=slug, post_subtitle=post_subtitle, category=category, post_posted_by=post_posted_by, post_desc=desc, stime=datetime.datetime.now())
        db.session.add(postobj)
        db.session.commit()
        return redirect('/dashboard')
    return render_template('addPost.html')

@app.route('/dashboard/addVideo', methods=["GET", "POST"]) # page for adding videos in db
def addvideo():
    if not('username' in session):
        return redirect('/admin')
    if request.method == 'POST':
        video_title = request.form.get('video_title')
        video_subtitle = request.form.get('video_subtitle')
        video_posted_by = request.form.get('video_posted_by')
        slug = request.form.get('slug')
        image = request.form.get('image')
        desc = request.form.get('desc')
        category = request.form.get('category')
        videoobj = Video(image=image, video_title=video_title, category=category, slug=slug,stime=datetime.datetime.now(), video_subtitle=video_subtitle, video_posted_by=video_posted_by, video_desc=desc)
        db.session.add(videoobj)
        db.session.commit()
        return redirect('/dashboard')
    return render_template('addvideo.html', postdata=Post.query.all())



# editing endpoints 
@app.route('/dashboard/editPost/<string:slug>', methods=["GET", "POST"]) # page for editing post in db
def editpost(slug):
    postsData = Post.query.filter_by(slug=slug).first()
    if not('username' in session):
        return redirect('/admin')
    if request.method == 'POST':
        post_title = request.form.get('post_title')
        post_subtitle = request.form.get('post_subtitle')
        post_posted_by = request.form.get('post_posted_by')
        slug = request.form.get('slug')
        desc = request.form.get('desc')
        category = request.form.get('category')
        postsData.post_title = post_title
        postsData.post_subtitle = post_subtitle
        postsData.post_posted_by = post_posted_by
        postsData.slug = slug
        postsData.post_desc = desc
        postsData.category = category
        db.session.commit()
        return redirect('/dashboard')
    return render_template('editPosts.html', postsData=postsData)

@app.route('/dashboard/editVideo/<string:slug>', methods=["GET", "POST"]) # page for editing videos in db
def editvideo(slug):
    videosData = Video.query.filter_by(slug=slug).first()
    if not('username' in session):
        return redirect('/admin')
    if request.method == 'POST':
        video_title = request.form.get('video_title')
        video_subtitle = request.form.get('video_subtitle')
        video_posted_by = request.form.get('video_posted_by')
        slug = request.form.get('slug')
        desc = request.form.get('desc')
        image = request.form.get('image')
        category = request.form.get('category')
        videosData.video_title = video_title
        videosData.video_subtitle = video_subtitle
        videosData.video_posted_by = video_posted_by
        videosData.slug = slug
        videosData.video_desc = desc
        videosData.image = image
        db.session.commit()
        return redirect('/dashboard')
    return render_template('editvideo.html', videoData=videosData)

# deleting endpints
@app.route('/dashboard/deletepost/<string:slug>', methods=["GET", "POST"]) # page for deleting post in db
def deletepost(slug):
    postsData = Post.query.filter_by(slug=slug).first()
    if not('username' in session):
        return redirect('/admin')
    db.session.delete(postsData)
    db.session.commit()
    return redirect('/dashboard')

@app.route('/dashboard/deletevideo/<string:slug>', methods=["GET", "POST"]) # page for deleting videos in db
def deletevideo(slug):
    videosData = Video.query.filter_by(slug=slug).first()
    if not('username' in session):
        return redirect('/admin')
    db.session.delete(videosData)
    db.session.commit()
    return redirect('/dashboard')
@app.route('/logout', methods=["GET", "POST"])

# Logout endpoint
def logout():
    session.pop('username', None)
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
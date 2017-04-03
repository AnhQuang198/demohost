from flask import *
from datetime import *
import mlab
from models.fooditem import fooditem
from models.user import User
import os
from werkzeug.utils import *
from flask_login import *
from sessionuser import SessionUser

app = Flask(__name__)

mlab.connect()
# new_food = fooditem()
# new_food.src = "https://www.w3schools.com/w3images/wine.jpg"
# new_food.title = "The Perfect Sandwich, A Real NYC Classic"
# new_food.description = "Just some random text, lorem ipsum text praesent tincidunt ipsum lipsum."
#
# new_food.save()

app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'upload')
if not os.path.exists(app.config['UPLOAD_PATH']):
    os.makedirs(app.config['UPLOAD_PATH'])

app.secret_key = 'quangdz'

login_manager = LoginManager()
login_manager.init_app(app)

# addmin_user = User()
# addmin_user.username = 'admin'
# addmin_user.password = 'admin'
# addmin_user.save()

@login_manager.user_loader
def user_loader(user_token):
    found_user = User.objects(token=user_token).first()
    if found_user:
        session_user = SessionUser(found_user.id)
        return session_user

@app.route('/')
def hello_world():
    return redirect(url_for('test1'))

#
# @app.route('/cssdemo')
# def cssdemo():
#     return render_template("cssdemo.html")
#
@app.route('/addFood', methods=["GET","POST"])
def addFood():
    if(request.method == "GET"):
        return render_template("addFood.html")
    if(request.method == "POST"):
        file = request.files['source']
        if file:
            filename = secure_filename(file.filename)
            if os.path.exists(os.path.join(app.config['UPLOAD_PATH'],filename)):
                name_index = 0

                #filename = home.png
                original_name = filename.rsplit('.', 1)[0]
                original_extension = filename.rsplit('.', 1)[1]
                while os.path.exists(os.path.join(app.config['UPLOAD_PATH'],filename)):
                    name_index += 1

                    #filrname = home(1).png
                    filename = "{0} ({1}).{2}".format(original_name, name_index, original_extension)

            file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            new_food = fooditem()
            new_food.src = url_for('uploaded_file', filename=filename)
            # new_food.image = request.files["image"]
            new_food.title = request.form["title"]
            new_food.description = request.form["description"]
            new_food.save()
            return render_template("addFood.html")

@app.route('/uploas/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/deletefood', methods=["GET","POST"])
def deletefood():
    if(request.method == "GET"):
        return render_template("deletefood.html")
    if(request.method == "POST"):
        new_food = fooditem.objects(title=request.form["title"]).first()
        if new_food is not None:
            new_food.delete()
            return render_template("deletefood.html")

@app.route('/updatefood', methods=["GET","POST"])
def updatefoot():
    if(request.method == "GET"):
        return render_template("updatefood.html")
    if (request.method == "POST"):
        new_image = fooditem.objects(title=request.form["title"]).first()
        if new_image is not None:
            new_image.src = request.form["source"]
            new_image.description = request.form["description"]
            new_image.save()
        return render_template("update_image.html")

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        user = User.objects(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            session_user = SessionUser(user.id)
            user.update(set__token=str(user.id))
            login_user(session_user)

            return redirect(url_for('addFood'))
        else:
            return render_template("login.html")

food_list = [
    {
        "src" : "https://www.w3schools.com/w3images/sandwich.jpg",
        "title" : "The Perfect Sandwich, A Real NYC Classic",
        "description" : "Just some random text, lorem ipsum text praesent tincidunt ipsum lipsum."
    },
    {
        "src" : "https://www.w3schools.com/w3images/steak.jpg",
        "title" : "Let Me Tell You About This Steak",
        "description" : "Once again, some random text to lorem lorem lorem lorem ipsum text praesent tincidunt ipsum lipsum."
    },
    {
        "src" : "https://www.w3schools.com/w3images/cherries.jpg",
        "title" : "Cherries, interrupted",
        "description" : "Lorem ipsum text praesent tincidunt ipsum lipsum."
    },
    {
        "src" : "https://www.w3schools.com/w3images/wine.jpg",
        "title" : "Once Again, Robust Wine and Vegetable Pasta",
        "description" : "Lorem ipsum text praesent tincidunt ipsum lipsum."
    }
]

@app.route('/test1')
def test1():
    return render_template("test1.html",food_list = fooditem.objects)


if __name__ == '__main__':
    app.run()

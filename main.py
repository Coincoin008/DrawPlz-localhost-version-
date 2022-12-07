from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from getPictures import *
from getAccounts import *
from updateLike import *
import ast
import json



UPLOAD_FOLDER = './Static'  # où on telecharge les fichiers (ici photos)
ALLOWED_EXTENSIONS = {'jpg'} # les extensions autorisées

def allowed_file(filename):                                                             # une fonction pour vérifier l'extensions
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS # j'ai pas trop compris comment 

app = Flask(__name__)  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = "fhjedqnjfq;ehfkjdsbv"

@app.route("/")
def index():
    IMAGES = getPictures() # on chope les images
    with open("./Data/pictures.json", 'r') as file:
        aa = json.loads(file.read())
    #print(aa)
    return render_template("index.html", images=IMAGES, nLikes=aa)


@app.route("/admin-connect")                             # La page pour se connecter en tant qu'admin
def admin_connect():                                     # -> form de connexion
    return render_template("form-to-connect-admin.html") # -> pour pouvoir ajouter / supprimer des photos


@app.route("/confirm-connect-admin", methods=["POST"])
def confirm_admin():
    accounts = getAdminAccount() # on chope les comptes admins
    name = request.form["admin-name"] # on chope le nom entré
    pw = request.form["admin-pw"] # on chope le mdp entré
    for admin_name in accounts:
        admin = accounts[admin_name]
        if admin["name"] == name: 
            if admin["password"] == pw:
                error = False            # Si le nom existe et le mdp correspond :
                url = "/admin-panel"     # -> il n'y a pas d'erreur
            else:
                error_name = "Mot de passe incorrect"  # Si le nom existe mais le mdp correspond pas :
                error = True                           # -> le mdp est incorrect donc erreur
                url = "/error-connecting-admin"
        else:
            error_name = "Ce nom n'existe pas"     # Si le nom n'existe pas
            error = True                           # -> il y a une erreur
            url = "/error-connecting-admin"
            
    if error:
        return redirect(url_for("error_admin", error=error_name))
    else :
        return redirect("/secret")

@app.route("/error-admin/<error>")
def error_admin(error):
    return render_template("error-in-connection.html", error=error)



@app.route("/secret", methods=['GET', 'POST']). # secret isnt the actual url but i prefer not to write it there 
def admin_panel():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' in request.files:  # si y'a un fichier à télecharger
            print("hhh")
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':     # si c'est pas un fichier vide
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename): 
                print(f"{file.filename} dea")
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # on sauvegarde le fichier
                with open("./Data/pictures.json", 'r') as file:
                    json_ = json.loads(file.read())
                
                json_[filename] = { "likes" : 0}

                with open("./Data/pictures.json", 'w') as file:
                    file.write(json.dumps(json_, sort_keys=True, indent=4))
        
        if "picture-to-delete" in request.form: # si y'a un fichier à supprimer
            pictureToDelete = request.form["picture-to-delete"] # on le chope
            os.remove(app.config['UPLOAD_FOLDER'] + "/" + pictureToDelete) # on le supprime
            with open("./Data/pictures.json", 'r') as file:
                json_ = json.loads(file.read())
                
            del json_[pictureToDelete]

            with open("./Data/pictures.json", 'w') as file:
                file.write(json.dumps(json_, sort_keys=True, indent=4))
            
            print("AAAAA -> " + pictureToDelete)
    return render_template("admin-panel.html", pictures=getPictures())


@app.route("/background_process_test")
def background_procces_test():
    picture = request.args.get("picture", "69144172515--EBB28FB6-BE36-48A3-B153-5E06675D88AE.jpg")
    like = request.args.get("like", "dd")
    print(f"AAAAA {picture} BBBBBB {like}")
    updateLike(picture, ast.literal_eval(like))
    print(bool(like))
    return redirect("/")



if __name__ == "__main__":
    app.run(host="localhost")

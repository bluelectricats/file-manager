from flask import Flask, request, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from models import Files, db
import os
import json
import datetime
import shutil
from services import paths_srv, files_srv

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

##Путь к ресурсам
os.makedirs(os.path.join(app.instance_path, 'resources'), exist_ok=True)
res_root=os.path.join(app.instance_path, 'resources')
paths=paths_srv()
path_tree=paths.get_paths(res_root)


@app.route('/',methods=["POST", "GET"])
def index():
    if request.method == "POST":
        f = request.files['file']
        file_name = secure_filename(f.filename)
        extract=os.path.splitext(file_name)
        #file_path=os.path.join(app.instance_path, 'resources')
        file_path=files_srv.manage_directories(res_root,extract[1])
        #f.save(os.path.join(app.instance_path, 'resources', file_name))
        f.save(os.path.join(file_path,file_name))
        created_on = datetime.datetime.now().isoformat()
        file_size=os.path.getsize(file_path+'\\'+file_name)
        new_file = Files(name=extract[0], extension=extract[1], size=file_size, path=file_path, created_on=created_on, commentary=request.form['commentary'])
        db.session.add(new_file)
        db.session.commit()
        return redirect("/")
    else:
        all_files = Files.query.all()
        json_list=[i.serialize for i in all_files]
        print(json.dumps(json_list))
        res=json.dumps(json_list)
        return render_template("index.html", all_files = all_files, path_tree=path_tree)

@app.route('/<id>/', methods=["GET","POST"])
def get_single_file(id):
    file = Files.query.get(id)
    json_list=file.serialize
    print(json.dumps(json_list))
    res=json.dumps(json_list)
    return render_template("single_file.html", file=file)
    
      
@app.route('/<path:path>')
def get_path(path):
    contains=[]
    path = path.replace("/", "\\")
    for address, dirs, files in os.walk(path):
        for name in files:
            contains.append(os.path.join(address, name))
    return render_template("directory.html", contains=contains, path=path)

   
@app.route('/update/<id>/', methods=["GET","POST"])
def update(id):
    file = Files.query.get(id)
    old_name=file.name
    if request.method=="POST":
        old_path=file.path
        new_path=request.form.get('directories')
        new_name=request.form.get('name')
        shutil.move(old_path+r'\\'+old_name+file.extension,new_path+r'\\'+new_name+file.extension)
        file.path=new_path     
        file.name=new_name
        file.changed_on = datetime.datetime.now().isoformat()       
        file.commentary=request.form.get('commentary')
        db.session.commit()
        return redirect('/')
    return render_template("update_file.html", path_tree=path_tree, fname=old_name)


@app.route('/delete/<id>/')
def delete(id):
    file = Files.query.get(id)
    full_fpath=file.path+file.name+file.extension
    if files_srv.check_if_exists(full_fpath):
        os.remove(full_fpath)
    db.session.delete(file)
    db.session.commit()
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)

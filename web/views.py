from flask import redirect, render_template, request, url_for
from web import app
from web.forms import UploadVideoForm
from web.models import Video

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html')



@app.route('/video', methods=['GET', 'POST'])
def video():

    video=Video.query.id()

    return render_template('video.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    form = UploadVideoForm(csrf_enabled=False)
    if form.validate_on_submit():
        print(form.name.data)
        print(dir(request.files))
        #if form.name.data not in request.files:
            #flash('No file part')
            #return redirect(request.url)
        file = request.files[form.name.data]
        print(file)
        if file.filename == '':
            #flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    
    return render_template('upload_video.html', form=form)


from flask import redirect, render_template, make_response
from web import app
from web.forms import UploadVideoForm
from web import ALLOWED_EXTENSIONS
from .helper import read_image
@app.route('/images/<int:pid>.jpg')
def get_image(pid):
    image_binary = read_image(pid)
    response = make_response(image_binary)
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='%s.jpg' % pid)
    return response

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/calibrate', methods=['GET', 'POST'])
def multicheck():
    return render_template('color.html', color="#FF0000")

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    form = UploadVideoForm(csrf_enabled=False)
    if request.method == 'POST':
        print('    ')
        print(request.files)
        print(form.name.data)
        print('    ')
        if 'name' not in request.files:
            #flash('No file part')
            print('YES')
            return redirect(request.url)
        file = request.files['name']
        print(file)
        if file.filename == '':
            #flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save('videos/' + filename)
            return redirect(request.url)
    #os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return render_template('upload_video.html', form=form)

@app.route('/rezult', methods=['GET', 'POST'])
def rezult():
    return render_template('rezult.html', pid=1)

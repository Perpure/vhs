from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FieldList, BooleanField, RadioField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from wtforms.widgets import CheckboxInput, ListWidget


class UploadVideoForm(FlaskForm):
    name = FileField("File", validators=[Length(3)])
    submit = SubmitField("Upload")


from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class EditClauseForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=1, max=100)])
    content = TextAreaField("Inclause", validators=[DataRequired(), Length(min=2)])
    submit = SubmitField("Update")


class InclauseForm(FlaskForm):
    inputdata = TextAreaField("Input list", validators=[DataRequired(), Length(min=2)])
    submit = SubmitField("Make In Clause")

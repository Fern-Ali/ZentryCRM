from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, validators, ValidationError, SelectField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Optional, Email, Length

class SearchForm(FlaskForm):
    '''searchform - site-wide - front-end'''
    query = StringField("query",
                       validators=[InputRequired()])
    submit = SubmitField("Submit")

class ProductForm(FlaskForm):
    """Form for adding playlists."""
    name = StringField("Name",
                       validators=[InputRequired()])
    #description = StringField("Description",
    #                    validators=[InputRequired()])
    sector_id = SelectField("Sector",
                              validators=[InputRequired()])
    category_id = SelectField("Category",
                              validators=[InputRequired()])
    
    strain_id = SelectField("Strain",
                              validators=[InputRequired()])
    seedling_id = SelectField("Seedling",
                              validators=[InputRequired()])
    plant_facility_id = SelectField("Plant Facility",
                              validators=[InputRequired()])
    


class CategoryForm(FlaskForm):
    """Form for adding/editing friend."""

    name = StringField("Category Name",
                       validators=[InputRequired()])
   




class RegisterForm(FlaskForm):
    """Form for adding/editing friend."""

    username = StringField("username",
                       validators=[InputRequired()])
    password = PasswordField("password",
                        validators=[InputRequired(), Length(min= 10, max= 500, message="More than 10 chars please")]) 
    email = StringField("email",
                        validators=[InputRequired(), Email()])
    image_url = StringField("image_url",
                        validators=[Optional()])

class LoginForm(FlaskForm):
    """Form for adding/editing friend."""

    username = StringField("username",
                       validators=[InputRequired()])
    password = PasswordField("password",
                        validators=[InputRequired()])
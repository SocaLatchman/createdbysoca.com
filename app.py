from flask import Flask, render_template, redirect, url_for
from sqlmodel import SQLModel, Session, select, Field, Relationship, create_engine
from sqlalchemy import event
from sqlalchemy.orm import selectinload
from flask_wtf import CSRFProtect
from email_validator import validate_email, EmailNotValidError
from passlib.hash import pbkdf2_sha256
from dotenv import load_dotenv 
from datetime import datetime, date
from flask_mailman import EmailMultiAlternatives, Mail
from typing import List, Optional
import os

load_dotenv('.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
app.config['MAIL_RECIPIENT'] = os.environ.get('MAIL_RECIPIENT')
csrf = CSRFProtect(app)
mail = Mail(app)
db_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)

class User(SQLModel, table=True):
    user_id: int = Field(default=None, primary_key=True)
    admin: str = Field(unique=True) 
    password: str
    last_active: datetime = Field(default_factory=date.today())
    image: str
    project_id: Optional[int] = Field(default=None, foreign_key="projects.project_id")
    image_id: Optional[int] = Field(default=None, foreign_key="images.image_id")

class Project(SQLModel, table=True):
    __tablename__ = 'projects'
    project_id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    category: str
    role: str
    url: str
    cover: str
    date_added: datetime = Field(default_factory=date.today())
    typefaces: List['Typography'] = Relationship(back_populates='project')
    colors: List['Color'] = Relationship(back_populates='project')
    logo: Optional['Logo'] = Relationship(back_populates='project')
    tags: List['Tag'] = Relationship(back_populates='project')

class Tag(SQLModel, table=True):
    __tablename__ = 'tags'
    tag_id: int = Field(default=None, primary_key=True)
    tag_name: str
    project_id: Optional[int] = Field(default=None, foreign_key='projects.project_id')
    project: Optional[Project] = Relationship(back_populates='tags')

class Typography(SQLModel, table=True):
    typography_id: int = Field(default=None, primary_key=True)
    font: str
    category: str
    weight: str
    project_id: Optional[int] = Field(default=None, foreign_key='projects.project_id')
    project: Optional[Project] = Relationship(back_populates='typefaces')

class Color(SQLModel, table=True):
    color_id: str = Field(default=None, primary_key=True)
    color: str
    hex_value: str
    role: str #button, background, accent color etc.
    project_id: Optional[int] = Field(default=None, foreign_key='projects.project_id')
    project: Optional[Project] = Relationship(back_populates='colors')

class Logo(SQLModel, table=True):
    logo_id: int = Field(default=None, primary_key=True)
    url: str
    project_id: Optional[int] = Field(default=None, foreign_key='projects.project_id')
    project: Optional[Project] = Relationship(back_populates='logo')

class Image(SQLModel, table=True):
    __tablename__ = 'images'
    image_id: int = Field(default=None, primary_key=True)
    url: str
    date_added: datetime = Field(default_factory=date.today())

class Portfolio:
    def get_portfolio(db_engine):
        try:
            with Session(db_engine) as session:
                statement = select(Project).options(
                selectinload(Project.typefaces),
                selectinload(Project.colors),
                selectinload(Project.logo),
                selectinload(Project.tags)
                )
                results = session.exec(statement).all()
                portfolio = []
                for project in results:
                    portfolio.append({
                        'project' : project.model_dump(),
                        'typography' : [typography.model_dump() for typography in project.typefaces],
                        'colors' : [color.model_dump() for color in project.colors],
                        'tag' : [tag.model_dump() for tag in project.tags],
                        'logo' : project.logo.model_dump() if project.logo else None
                    })
                return portfolio
        except Exception as e:
            return f'Unable to connect: {e}', 404

#enforce foreign keys when you use the engine(or session is created from db_engine)
def enforce_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

event.listen(db_engine, "connect", enforce_foreign_keys)

def create_db_and_tables():
   SQLModel.metadata.create_all(db_engine)

@app.route('/')
def home():
    portfolio = Portfolio.get_portfolio(db_engine)
    return render_template('index.html', title='Portfolio of Soca Latchman')

@app.route('/about')
def about():
    pass

@app.route('/contact')
def contact():
    pass

@app.route('/resume')
def resume():
    pass

@app.route('/blog')
def blog():
    pass

@app.route('/blog/post/<post_id>')
def blog_post():
    pass

@app.route('/project/<project_name>')
def project(project_name):
    return render_template('project.html', title='Projects created by Soca Latchman')

@app.route('/projects')
def projects():
    '''Return list of dictionaries'''
    pass

@app.route('/cms/signin')
def signin():
    return render_template('cms/signin.html')

@app.route('/cms/passcode', methods=['GET','POST'])
def cms_passcode():
    return render_template('cms/passcode.html')

@app.route('/cms')
def cms():
    return render_template('cms/index.html')


if __name__ == '__main__':
    create_db_and_tables()
    app.run(debug=True)
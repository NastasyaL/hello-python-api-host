from flask_restx import Resource, Namespace

from .models import Course, Student
from .api_models import course_model,student_model, course_input_model, student_input_model
from .extensions import db

ns = Namespace("api")

@ns.route("/hello")
class Hello(Resource):
    def get(self):
        return {"hello": "restx"}

@ns.route("/courses")
class CourseListAPI(Resource):
    @ns.marshal_list_with(course_model)
    def get(self):
        return Course.query.all()
    @ns.expect(course_input_model)
    @ns.marshal_with(course_model)
    def post(self):
        print(ns.payload)
        course = Course(name=ns.payload["name"])
        db.session.add(course)
        db.session.commit()
        return course,201

@ns.route("/courses/<int:id>")
class CourseAPI(Resource):
    @ns.marshal_with(course_model)
    def get(self, id):
        course = Course.query.get(id)
        return course    
@ns.route("/students")
class StudentAPIList(Resource):
    @ns.marshal_list_with(student_model)
    def get(self):
        return Student.query.all()
    @ns.expect(student_input_model)
    @ns.marshal_with(student_model)
    def post(self):
        print(ns.payload)
        student = Student(name=ns.payload["name"], course_id=ns.payload["course_id"])
        db.session.add(student)
        db.session.commit()
        return student, 201
    
@ns.route("/students/<int:id>")
class StudentAPI(Resource):
    @ns.marshal_with(student_model)
    def get(self, id):
        student = Student.query.get(id)
        return student  
    @ns.marshal_with(student_model)
    @ns.expect(student_input_model)
    def post(self, id):
        student = Student.query.get(id)
        student.name = ns.payload["name"]
        student.course_id = ns.payload["course_id"]
        db.session.commit()
        return student


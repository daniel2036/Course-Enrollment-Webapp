from flask import Flask, redirect, render_template, request
from model import *
import matplotlib.pyplot as plt
import io
import base64


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///database.sqlite3"

db.init_app(app)

app.app_context().push()

@app.route('/')
def home():
    s=Student.query.all()
    return render_template('index.html',list=s)

@app.route('/courses')
def courses():
    s=Course.query.all()
    return render_template('courses.html',list=s)

@app.route('/student/<int:student_id>/delete',methods=['GET','POST'])
def delete(student_id):
    student=Student.query.get(student_id)
    db.session.delete(student)
    enrol=Enrollments.query.filter_by(estudent_id=student_id).all()
    for i in enrol:
        db.session.delete(i)
    db.session.commit()
    return redirect('/')



@app.route('/student/<int:student_id>/update', methods=['GET', 'POST'])
def update(student_id):
    if request.method == 'POST':
        fname = request.form.get('f_name')
        lname = request.form.get('l_name')
        courses = request.form.getlist('courses')

        student = Student.query.get(student_id)
        if student:
            if fname != 'current_f_name':
                student.first_name = fname
            if lname != 'current_l_name':
                student.last_name = lname

            # Remove existing enrollments
            Enrollments.query.filter_by(estudent_id=student_id).delete()

            # Add new enrollments
            for c in courses:
                e = Enrollments(estudent_id=student_id, ecourse_id=c)
                db.session.add(e)

            db.session.commit()
            return redirect('/')

    else:
        student = Student.query.get(student_id)
        if student:
            courses = Course.query.all()
            return render_template('update.html', student=student, courses=courses)

@app.route('/student/<int:student_id>')
def details(student_id):
    s=Student.query.get(student_id)
    list=s.courses
    return render_template('details.html',list=list,s=s)

@app.route('/course/<int:course_id>', methods=['GET'])
def course_details(course_id):
    # Fetch course details
    course = Course.query.get(course_id)

    # Fetch enrollment details for the course
    enrollments = Enrollments.query.filter_by(ecourse_id=course_id).all()

    # Fetch student details for the enrolled students
    students = []
    for enrollment in enrollments:
        student = Student.query.get(enrollment.estudent_id)
        if student:
            students.append(student)

    return render_template('course_details.html', course=course, students=students)

@app.route('/student/create',methods=['GET','POST'])
def add_student():
    if request.method=="POST":
        roll=request.form.get('roll')
        fname=request.form.get('f_name')
        lname=request.form.get('l_name')
        courses=request.form.getlist('courses')
        r=Student.query.filter_by(roll_number=roll).all()
        for i in r:
            if i.roll_number==roll:
                return render_template('exist.html')
        s=Student(roll_number=roll,first_name=fname,last_name=lname)
        db.session.add(s)
        db.session.commit()
        q=Student.query.filter_by(roll_number=roll).first()
        for c in courses:
            e=Enrollments(estudent_id=q.student_id,ecourse_id=c)
            db.session.add(e)
        db.session.commit()
        return redirect('/')
  
    else:
        courses = Course.query.all()
        return render_template('create_student.html',courses = courses)
    
@app.route('/course/create',methods=['GET','POST'])
def add_courses():
    if request.method=="POST":
        code=request.form.get('code')
        c_name=request.form.get('c_name')
        desc=request.form.get('desc')
        r=Course.query.filter_by(course_code=code).all()
        for i in r:
            if i.course_code==code:
                return render_template('course_exist.html')
        s=Course(course_code=code,course_name=c_name,course_description=desc)
        db.session.add(s)
        db.session.commit()
        return redirect('/')  
    else:
        return render_template('create_course.html')
    
@app.route('/course/<int:course_id>/update', methods=['GET', 'POST'])
def course_update(course_id):
    if request.method == 'POST':
        code = request.form.get('code')
        c_name = request.form.get('c_name')
        desc = request.form.get('desc')

        course = Course.query.get(course_id)
        if code != 'current_code':
            course.course_code = code
        if c_name != 'current_c_name':
            course.course_name = c_name
        course.course_description = desc        
       

        db.session.commit()
        return redirect('/courses')
    else:
        # Fetch course details and enrolled students for rendering the update form
        course = Course.query.get(course_id)
        enrolled_students = Enrollments.query.filter_by(ecourse_id=course_id).all()
        return render_template('course_update.html', course=course, enrolled_students=enrolled_students)



@app.route("/student/<int:student_id>/withdraw/<int:course_id>",methods=['GET','POST'])
def withdraw(student_id, course_id):
    course=Course.query.get(course_id)
    enrol=Enrollments.query.filter_by(estudent_id=student_id, ecourse_id = course_id).all()
    for i in enrol:
        db.session.delete(i)
    db.session.commit()
    return redirect('/')

@app.route('/course/<int:course_id>/delete',methods=['GET','POST'])
def course_delete(course_id):
    course=Course.query.get(course_id)
    db.session.delete(course)
    enrol=Enrollments.query.filter_by(ecourse_id=course_id).all()
    for i in enrol:
        db.session.delete(i)
    db.session.commit()
    return redirect('/courses')

# Function to generate pie chart for number of subjects taken by students
def generate_subjects_pie_chart():
    # Collect data - Example: Get the count of subjects taken by each student
    subjects_counts = db.session.query(Student, db.func.count(Enrollments.ecourse_id)).join(Enrollments).group_by(Student.student_id).all()
    
    # Process data to calculate distribution
    subjects_distribution = {}
    for student, count in subjects_counts:
        if count not in subjects_distribution:
            subjects_distribution[count] = 1
        else:
            subjects_distribution[count] += 1
    
    # Create labels and sizes for pie chart
    labels = [f"{count} subjects" for count in subjects_distribution.keys()]
    sizes = list(subjects_distribution.values())
    
    # Create pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Distribution of Students by Number of Subjects')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    
    # Save plot to buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    
    # Encode plot as base64 string
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')
    return plot_data

@app.route('/dashboard')
def dashboard():
    # Generate pie chart for number of subjects taken by students
    subjects_pie_chart = generate_subjects_pie_chart()
    
    return render_template('dashboard.html', subjects_pie_chart=subjects_pie_chart)

if __name__=='__main__':
    app.run()


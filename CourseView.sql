-- SQLite
DROP VIEW IF EXISTS vEnrollments;
 
CREATE TABLE student (
	student_id INTEGER NOT NULL, 
	roll_number VARCHAR NOT NULL, 
	first_name VARCHAR NOT NULL, 
	last_name VARCHAR, email varchar(250), 
	PRIMARY KEY (student_id), 
	UNIQUE (roll_number)
) 

CREATE TABLE course (
	course_id INTEGER NOT NULL, 
	course_code VARCHAR NOT NULL, 
	course_name VARCHAR NOT NULL, 
	course_description VARCHAR, 
	PRIMARY KEY (course_id), 
	UNIQUE (course_code)
)

CREATE TABLE enrollments (
	enrollment_id INTEGER NOT NULL, 
	estudent_id INTEGER NOT NULL, 
	ecourse_id INTEGER NOT NULL, 
	PRIMARY KEY (enrollment_id), 
	FOREIGN KEY(estudent_id) REFERENCES student (student_id), 
	FOREIGN KEY(ecourse_id) REFERENCES course (course_id)
)

-- CREATE VIEW vEnrollments AS 
-- SELECT std.first_name,std.last_name, crs.Course_code,crs.course_description  from enrollments er 
-- join student std on er.estudent_id  = std.student_id
-- join course crs on er.ecourse_id = crs.course_id order by first_name;

 
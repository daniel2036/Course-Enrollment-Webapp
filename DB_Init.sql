CREATE TABLE student (
	student_id INTEGER NOT NULL, 
	roll_number VARCHAR NOT NULL, 
	first_name VARCHAR NOT NULL, 
	last_name VARCHAR, email varchar(250), 
	PRIMARY KEY (student_id), 
	UNIQUE (roll_number)
) ;

CREATE TABLE course (
	course_id INTEGER NOT NULL, 
	course_code VARCHAR NOT NULL, 
	course_name VARCHAR NOT NULL, 
	course_description VARCHAR, 
	PRIMARY KEY (course_id), 
	UNIQUE (course_code)
);

CREATE TABLE enrollments (
	enrollment_id INTEGER NOT NULL, 
	estudent_id INTEGER NOT NULL, 
	ecourse_id INTEGER NOT NULL, 
	PRIMARY KEY (enrollment_id), 
	FOREIGN KEY(estudent_id) REFERENCES student (student_id), 
	FOREIGN KEY(ecourse_id) REFERENCES course (course_id)
);

INSERT into course (course_code,course_name,course_description)
VALUES ('BST13','BDM','Business Data Management'),
('NDAB21010U','DIS','Databases and Information Systems. This course introduces students to basic database concepts such as relational databases, normal forms, and transactions. In addition, the course covers system development (basic software development) and version control and includes the practical development of a smaller system (web system, mobile system, or the like, which must be decided before the course starts) as project work. Formal languages and reading of structured text are also covered.'),
('NDAB22007U','Software Development for Digital Health','The course provides an introduction to the elementary elements in the development of IT systems in the healthcare system. The course focuses on system development and software engineering techniques: requirements specification, basic UML diagrams and system development methods.  As software integrates with information systems, the student will acquire skills in modelling and manipulation of data in relational databases. Finally, the course will equip the student with skills in data communication via information exchange.'),
('HDCB01152U','DCC Nordic Mythology','Nordic Mythology is a course in English for international students. It is a course within the science of religion, and it deals with the religion in Denmark before the introduction of Christianity. In the course we will read some poems concerning pre-Christian deities from Iceland as well as the medieval Icelandic writer Snorri, which makes it possible to get a glimpse of the mythology of the Scandinavians before Christianity. The gods Odin, Thor, Vanir, Loki and Balder will be accentuated. We will also go beyond mythology and try to get an idea about the religious rituals and the religious experts of the Norsemen. The course includes excursions to the Viking Ship Museum in Roskilde and a very popular excursion to Scania, where we will visit a couple of burial places in the shape of a ship and also some well-preserved runic stones.');

-- DROP VIEW IF EXISTS vEnrollments;

-- CREATE VIEW vEnrollments AS 
-- SELECT std.first_name,std.last_name, crs.Course_code,crs.course_description  from enrollments er 
-- join student std on er.estudent_id  = std.student_id
-- join course crs on er.ecourse_id = crs.course_id order by first_name;

 
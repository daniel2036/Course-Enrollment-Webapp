-- SQLite
SELECT std.first_name,std.last_name, crs.Course_code,crs.course_description  from enrollments er 
join student std on er.estudent_id  = std.student_id
join course crs on er.ecourse_id = crs.course_id;

select * from course;
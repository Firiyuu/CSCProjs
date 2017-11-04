from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)


# UNCOMMENT TO CREATE NEW TABLE
# studentRecord= students table
# courseList = coursee table
# studlis

#conn = sql.connect('database.db')
#print "Opened database successfully";
#conn.execute('CREATE TABLE IF NOT EXISTS courseEndedst(courseID TEXT, course TEXT, courseCode TEXT NOT NULL PRIMARY KEY, FOREIGN KEY (courseCode) REFERENCES StudentEndeds(course))')
#conn.execute('CREATE TABLE IF NOT EXISTS StudentEndedst(name TEXT, id TEXT PRIMARY KEY, course TEXT, year TEXT, gender TEXT)')



#print "Table created successfully";
#conn.close()






def add_entry(stud):
    conn = sql.connect('database.db')
    cur = conn.cursor()

    cur.execute("INSERT INTO StudentEndedst(name,id,course,year, gender) VALUES (?,?,?,?,?)",
                (stud.nm, stud.idno, stud.course, stud.year, stud.gender))

    cur.execute("SELECT*FROM StudentEndedst")
    for row in cur.fetchall():
        print (row)
    conn.commit()
    conn.close()

def add_courseentry(crse):
    conn = sql.connect('database.db')
    cur = conn.cursor()

    cur.execute("INSERT INTO courseEndedst(courseID,course,courseCode) VALUES (?,?,?)",
                (crse.courseID, crse.course, crse.courseCode))

    cur.execute("SELECT*FROM courseEndedst")
    for row in cur.fetchall():
        print (row)
    conn.commit()
    conn.close()


class Student(object):
    def __init__(self, nm, idno, course, year, gender):
        self.nm = nm
        self.idno = idno
        self.course = course
        self.year = year
        self.gender = gender



class Course(object):
    def __init__(self, courseID, course, courseCode):
        self.courseID = courseID
        self.course = course
        self.courseCode = courseCode


@app.route('/')
def home():
    return render_template('index.html')






@app.route('/courses')
def courses():
    return render_template('course.html')


@app.route('/courserec', methods=['POST', 'GET'])
def courserec():
    if request.method == 'POST':
        courseid = request.form['courseID']
        course = request.form['course']
        coursecode = request.form['courseCode']

        crse = Course(courseid, course, coursecode)
        add_courseentry(crse)
        msg = "Record successfully added"

        return render_template("courseresult.html", msg=msg)

# ADD
@app.route('/register')
def register():
    return render_template('test.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':

            nm = request.form['nm']
            idno = request.form['id']
            course = request.form['course']
            year = request.form['year']
            gender = request.form['gender']


            stud = Student(nm, idno, course, year,gender)
            add_entry(stud)
            msg = "Record successfully added"

            return render_template("result.html",msg=msg)



@app.route('/deletecourse')
def deletecourse():
    return render_template('deletecourse.html')


@app.route('/delreccourse', methods=['POST', 'GET'])
def delreccourse():
    if request.method == 'POST':
        try:

            idsearch = request.form['idsearch']

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(("DELETE FROM courseEndedst WHERE courseID= ?"), [idsearch])

                con.commit()
                msg = "Record successfully deleted"
        except:
            con.rollback()
            msg = "Error"

        finally:
            return render_template("delresultcourse.html", msg=msg)
            con.close()



@app.route('/delete')
def delete():
    return render_template('deletestud.html')


@app.route('/delrec', methods=['POST', 'GET'])
def delrec():
    if request.method == 'POST':
        try:

            idsearch = request.form['idsearch']

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(("DELETE FROM StudentEndedst WHERE id= ?"), [idsearch])

                con.commit()
                msg = "Record successfully deleted"
        except:
            con.rollback()
            msg = "Error"

        finally:
            return render_template("delresult.html", msg=msg)
            con.close()


# UPDATE



@app.route('/update/')
def update():
    return render_template("updatestud.html")


@app.route('/update_form/', methods=['POST', 'GET'])
def update_form():
    if request.method == 'POST':

        ids = request.form['id_search']
        print ids
        print "something"
        with sql.connect("database.db") as conn:
           cur = conn.cursor()
           cur.execute("SELECT * FROM StudentEndedst")
           rows = cur.fetchall()
           print rows
           for row in rows:
              print row
              if row[1] == ids:
                 copied = row
                 msg = "Student Found"
                 break
              else:
                 msg = "Student Not Found"
                 copied = " "

        return render_template("newform.html", msg=msg, copied=copied)






@app.route('/success', methods=['POST', 'GET'])
def success():
    if request.method == 'POST':

        nm = request.form['nm']
        print nm
        idno = request.form['id']
        print idno
        crse = request.form['course']
        print crse
        yr = request.form['year']

        gender = request.form['gender']
        print yr


        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM StudentEndedst")
            rows = cur.fetchall()
            print "somethng"
            print rows
            for row in rows:
                print rows
                print row[1]
                print row[0]

                if row[1] == idno:
                    cur.execute("UPDATE StudentEndedst SET name = ?, course= ?, year = ?, gender = ? WHERE id = ?", (nm, crse, yr, gender, idno))
                    con.commit()
                    msg = "Success"
                else:
                    msg = "Fail"


        return render_template('updresult.html', msg=msg)


@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("SELECT * from StudentEndedst")

    rows = cur.fetchall();
    return render_template("listest.html", rows=rows)

@app.route('/courselist')
def courseList():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("SELECT * from courseEndedst")

    rows = cur.fetchall();
    return render_template("courselist.html", rows=rows)



@app.route('/querycourse',methods=['POST', 'GET'])
def querycourse():
    return render_template('querycourse.html')

@app.route('/queryrec', methods=['POST', 'GET'])
def queryrec():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    ids = request.form['coursesearch']

    with sql.connect("database.db") as conn:
        cur = conn.cursor()
        con.execute("CREATE VIEW IF NOT EXISTS result AS SELECT name, id, course, year, gender FROM StudentEndedst CROSS JOIN courseEndedst WHERE courseEndedst.course = StudentEndedst.course")
        cur.execute("SELECT * FROM result")
        rows = cur.fetchall()



    return render_template("listquery.html", rows=rows)
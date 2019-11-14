from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from models import User, Course, Student, StaffMember, Semester, Requirement
from query_factory import QueryFactory
from datetime import datetime

app = Flask(__name__)
CORS(app, support_credentials=True)
query_factory = QueryFactory()
query_factory.initialize_connection(db_name="cmp", db_user="postgres", db_password="")


@app.route('/StudentCourse', methods=['GET'])
def StudentCourse():
    dataa = request.get_json()
    studentid = 1
    username = request.args.get('username')
    dataa  = query_factory.getCourses(username)
    data = []
    for x in dataa:
        dec = {}
        dec["code"]  = x[0]
        dec["name"] = x[1]
        data.append(dec)
    print(data)
    return jsonify(data)

@app.route('/StudentRequirement',methods=['POST'])
def studentRequirement():
    recvdata =request.get_json()
    id = recvdata.get('id')
    dataa = query_factory.getRequirements(id)
    print(dataa)
    data = []
    for x in dataa:
        dec = {}
        dec["reqName"] = x[0]
        dec["projName"] = x[1]
        dec["reqID"] = x[2]
        data.append(dec)
    print(data)
    return jsonify(data)

@app.route('/stdReq',methods=['GET','PUT'])
def stdReq():
    if request.method == 'GET':
        recvdata =request.get_json()
        reqid = request.args.get('reqID')
        dataa = query_factory.getReqById(reqid)
        print(dataa)
        data = []
        for x in dataa:
            dec = {}
            dec["reqID"] = x[0]
            dec["cCode"] = x[1]
            dec["projID"] = x[2]
            dec["reqName"] = x[3]
            dec["deadline"] = x[4]
            dec["additionalMaterial"] = x[5]
            dec["document"] = x[6]
            dec["type"] = x[7]
            if x[9] == None:
                dec["lower"] =  None
                dec["upper"] = None
            else:
                dec["lower"] = x[9]
                dec["upper"] = x[10] - 1
            dec["cName"] = x[11]
            dec["projName"] = x[12]
            data.append(dec)
        print('REQUIREMENT:', data)
        return jsonify(data)
    if request.method == 'PUT':
        data = request.get_json()
        reqID = data.get('reqID')
        name = data.get('name')
        deadline = data.get('deadline')
        addMaterials = data.get('addMaterials')
        document = data.get('document')
        response = query_factory.updateReqbyStaff(reqID,name,deadline,addMaterials,document)
        return jsonify(response)


@app.route('/inTeam',methods=['GET'])
def inTeamb():
    recvdata =request.get_json()
    reqid = request.args.get('reqID')
    username = request.args.get('username')
    data = query_factory.isInTeam(reqid,username)
    return jsonify(data)

@app.route('/TeamInfo',methods=['GET'])
def TeamInfo():
    recvdata =request.get_json()
    reqid = request.args.get('reqID')
    username = request.args.get('username')
    stdsdata = query_factory.getStudentsInTeamInfo(reqid,username)
    teamdata = query_factory.getTeamInfo(reqid,username)
    print(stdsdata)
    print(teamdata)

    studentsdata = []
    for x in stdsdata:
        dec = {}
        dec["stdName"] = x[0]
        dec["stdSec"] = x[1]
        dec["stdBN"] = x[2]
        dec["stdUsername"] = x[3]
        dec["email"] = x[4]
        studentsdata.append(dec)
    if teamdata != []:
        dec2 = {}
        dec2["tmName"] =teamdata[0][0]
        dec2["tmNumber"] =teamdata[0][1]
        dec2["tmId"] =  teamdata[0][2]
    else:
        dec2 = {}
        dec2["tmName"] =None
        dec2["tmNumber"] =None
        dec2["tmId"] =  None

    wholedata = {}
    wholedata["Students"] = studentsdata
    wholedata["Team"] = dec2
    print(wholedata)
    return jsonify(wholedata)

@app.route('/noTeamStdInfo',methods=['GET'])
def noTeamStudentsInfo():
    recvdata =request.get_json()
    reqid = request.args.get('reqID')
    username = request.args.get('username')
    stddata = query_factory.getStudentsNotInTeam(reqid,username)
    print(stddata)
    data = []
    if stddata != []:
        for x in stddata:
            dec = {}
            dec["stdId"] = x[0]
            dec["stdName"] = x[1]
            data.append(dec)
    else:
        data = stddata
    print(data)
    return jsonify(data)

@app.route('/AddTeam',methods=['GET', 'POST'])
def isTeamNumberavilable():
    if request.method == 'GET':
        reqid = request.args.get('reqID')
        tmn = request.args.get('tmno')
        data = query_factory.isTeamNoAvilabe(reqid,tmn)
        print(data)
        return jsonify(data)

    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        courseCode = data.get('courseCode')
        reqID = data.get('requirementID')
        teamNumber = data.get('teamNumber')
        teamName = data.get('teamName')
        (is_successful, teamID) = query_factory.addTeam(courseCode, reqID, teamNumber, teamName)
        studentsIDs = data.get('studentIDs')
        creatorID = query_factory.get_student_id(username)
        if creatorID is None:
            is_successful = False
            message = 'Team could not be created.'
        else:
            studentsIDs.append(creatorID)
            is_successful = is_successful and query_factory.fillTeamMembers(teamID, studentsIDs)
            if is_successful:
                message = "Team created successfully."
            else:
                message = "Team could not be created."
        response = {'is_successful': is_successful, 'message': message}
        return jsonify(response)
@app.route('/deliverable',methods=['GET', 'POST'])
def deliverabledata():
    if request.method == 'GET':
        username = request.args.get('username')
        reqID = request.args.get('reqID')
        teamID = request.args.get('teamID')

        print(f"username:{username} //  reqID:{reqID} // teamid:{teamID}")
        print("//////////////////////////////////////////////////////////")
        print("//////////////////////////////////////////////////////////")
        dedata = query_factory.deliverableShit(reqID,username,teamID)
        print(dedata)
        dec = {}
        if dedata != []:
            dec["is_delivered"] = True
            dec["dID"] = dedata[0][0]
            dec["disPublic"] = dedata[0][1]
            dec["dmaterials"] = dedata[0][2]
            dec["feedback"] = dedata[0][3]
            dec["sID"] = dedata[0][4]
            dec["sName"] = dedata[0][5]
        else:
            dec["is_delivered"] = False
        print(dec)
        return jsonify(dec)
    if request.method == 'POST':
        data = request.get_json()
        req_id = data.get('req_id')
        cCode = data.get('cCode')
        materials = data.get('materials')
        tmID = data.get('tmID')
        username = data.get('username')
        delivery_time = datetime.now()
        response = query_factory.adddeliverable(req_id,cCode,materials,delivery_time,tmID,username)
        return jsonify(response)

@app.route('/staffcourses',methods=['GET'])
def getstaffCourses():
    if request.method == 'GET':
        username = request.args.get('username')
        dataa = query_factory.getstaffCourses(username)
        data = []
        if dataa != []:
            for x in dataa:
                dec = {}
                dec["cCode"] = x[0]
                dec["cName"] = x[1]
                data.append(dec)
            print(data)
        else:
            print("///////////////////////////////nothin was returned////////////")
        return jsonify(data)

@app.route('/staffReqBycCode',methods=['GET','POST'])
def reqrelatedToStaff():
    if request.method == 'GET':
        cCode = request.args.get('cCode')
        d = query_factory.getreqbyCourseCode(cCode)
        dataa = d["RDATA"]
        data = []
        if dataa!= []:
            for x in dataa:
                dec = {}
                dec["reqID"] = x[0]
                dec["reqName"] = x[1]
                dec["projName"] = x[2]
                dec["projID"] = x[3]
                data.append(dec)
            print(data)
        else:
            print("//////////////////no requirments for this course")
        pdataa = d["PData"]
        pdata = []
        if pdataa != []:
            for y in pdataa:
                dec = {}
                dec["projName"] = y[0]
                dec["projID"] = y[1]
                pdata.append(dec)
        else:
            print("//////////////////no projects for this course")
        wholedata = {
        "RDATA":data,
        "PDATA":pdata
        }
        print("/////////////////////////////////////////////////////////////////////////////////////////////")
        print(wholedata)
        return jsonify(wholedata)
    if request.method == 'POST':
        data = request.get_json()
        insertionType = data.get('insertionType')
        cCode = data.get('cCode')
        ProjectID = data.get('ProjectID')
        ProjectName = data.get('ProjectName')
        ProjectDocument = data.get('ProjectDocument')
        Name = data.get('Name')
        DeadLine = data.get('DeadLine')
        addMaterials = data.get('addMaterials')
        document = data.get('document')
        type = data.get('type')
        minNumber = data.get('minNumber')
        maxNumber = data.get('maxNumber')
        response = query_factory.addnewReqByStaff_member(insertionType,cCode,ProjectID,ProjectName,ProjectDocument,Name,DeadLine,addMaterials,document,type,minNumber,maxNumber)
        print(response)
        return jsonify(response)

@app.route('/unAssignedReqStaff',methods=['GET','POST','DELETE'])
def unAssignedReqStaff():
    if request.method == 'GET':

        cCode = request.args.get('cCode')
        print("////////////////////////////////////App////////////////////////////////////")
        print(cCode)
        print("////////////////////////////////////App////////////////////////////////////")
        dataa = query_factory.getUnassignedRequirements(cCode)
        data = []
        if dataa != []:
            for x in dataa:
                dec = {}
                dec["reqName"] = x[0]
                dec["reqID"] = x[1]
                dec["projectName"] = x[2]
                data.append(dec)
        else:
            print("NoReq Came back to be added brooooooo")
        print(data)
        return jsonify(data)
    if request.method == 'POST':
        data = request.get_json()
        cCode = data.get('cCode')
        reqID = data.get('reqID')
        respone = query_factory.assignReqbyStaff(cCode,reqID)
        print(respone)
        return jsonify(respone)
    if request.method == 'DELETE':
        reqID = request.args.get('reqID')
        data = query_factory.deleteReqbyStaff(reqID)
        print(data)
        return jsonify(data)

@app.route('/deliverablesStaff',methods=['GET','PUT','DELETE'])
def dealWithDeliverables():
    if request.method == 'GET':
        cCode = request.args.get('cCode')
        reqID = request.args.get('reqID')
        data = query_factory.getDeliverAblesbyStaff(reqID,cCode)
        print(data)
        return jsonify(data)
    if request.method == 'PUT':
        data = request.get_json()
        deliverableID = data.get('deliverableID')
        deliverableData = data.get('deliverableData')
        staffusername = data.get('staffusername')
        response = query_factory.addFeedbackbyStadd(deliverableID,deliverableData,staffusername)
        print(response)
        return jsonify(response)
    if request.method == 'DELETE':
        cCode = request.args.get('cCode')
        reqID = request.args.get('reqID')
        data = query_factory.unassignReqbyStaff(reqID,cCode)
        print(data)
        return jsonify(data)
@app.route('/teamsinDeliverables',methods=['GET','DELETE'])
def dealWithTeamsinDeliverables():
    if request.method == 'GET':
        cCode = request.args.get('cCode')
        reqID = request.args.get('reqID')
        dataa = query_factory.getTeamsINRequirement(reqID,cCode)
        data = []
        if dataa != []:
            for x in dataa:
                dec = {}
                dec["teamID"] = x[0]
                dec["teamNumber"] = x[1]
                dec["teamName"] = x[2]
                data.append(dec)
        print(data)
        return jsonify(data)
    if request.method == 'DELETE':
        teamID = request.args.get('teamID')
        response = query_factory.deleteTeam(teamID)
        print(response)
        return jsonify(response)


@app.route('/deleteDeliverable',methods=['DELETE'])
def deleteDeliverable():
    if request.method == 'DELETE':
        delivID = request.args.get('deliverableID')
        response = query_factory.deleteDeliverable(delivID)
        print(response)
        return jsonify(response)


@app.route( '/login' ,methods = ['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    is_user = query_factory.is_user(User(username=username, password=password))
    if is_user==False:
        res = {'username': False}
        return jsonify(res)
    [row] = is_user
    res = {'username': row[0], 'password': row[1], 'email': row[2], 'type': row[3]}
    return jsonify(res)


@app.route('/retrieve_account', methods=['POST'])
def retrieve_account():
    data = request.get_json()
    email = data.get('email')
    avi_email = query_factory.avi_email(User(email=email))
    res = {'check': avi_email}
    return jsonify(res)


@app.route('/change_password', methods=['PATCH'])
def change_password():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    pss = query_factory.update_password(User(email=email, password=password))
    res = {'check': pss}
    return jsonify(res)

@app.route('/Account', methods=['GET'])
def fill_account():
    username = request.args.get('username')
    flag= query_factory.Get_ALL(User(username=username))
    [row]=flag
    res = {'username': row[0],'password':row[1],'email':row[2],'type':row[3]}
    return jsonify(res)

@app.route('/Account_update', methods=['PATCH'])
def Update_account():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    oldusername = data.get('oldusername')
    if oldusername==username:
        check = query_factory.update_User(User(username=username, email=email, password=password), oldusername)
        res = {'check': check}
        return jsonify(res)

    check = query_factory.Get_ALL(User(username=username))
    if check:
        res = {'check':False}
        return jsonify(res)
    else:
      check = query_factory.update_User(User(username=username,email=email, password=password), oldusername)
      res = {'check': check}
      return jsonify(res)

@app.route('/home', methods=['GET'])
def fill_home():
    username = request.args.get('username')
    notfs = query_factory.GET_NOTIFICATIONS(username)
    print(notfs,f"came from database")
    if notfs==False:
        res = {'id':False}
        return jsonify(res)
    notfs_list = []
    for notf in notfs:
        notf_dict={'id':notf[1],'notf': notf[0]}
        notfs_list.append(notf_dict)

    print(notfs_list)

    return jsonify(notfs_list)

@app.route('/delete_notifications', methods=['DELETE'])
def delete_notifications():
    data = request.get_json()
    print(data,f"fisrt in back end")
    username = data.get('username')
    id = data.get('id')
    print(username,id)
    check = query_factory.Delete_NOTIFICATIONS(username, id)
    res={'check':check}
    print(res)
    return jsonify(res)

@app.route('/Portfolio', methods=['GET'])
def fill_portfolio():
    username = request.args.get('username')
    id = request.args.get('id')
    items = query_factory.get_portfolio(username,id)
    if items == False:
        res = [{'coursename': False}]
        print(res)
        return jsonify(res)

    p_list = []
    for item in items:
        portfolio_dict = {'coursename': item[0], 'projectname': item[1], 'reqname': item[2], 'material': item[3],
                          'type': item[4], 'teamname': item[5], 'feedback': item[6], 'sem': item[7],
                          'year': item[8]}
        p_list.append(portfolio_dict)

    print(p_list)
    return jsonify(p_list)
@app.route('/getdeliverbleCourse',methods=['GET'])
def getdeliverbleCourse():
    username=request.args.get('username')
    items = query_factory.get_portfoliocourses(username)
    if items == False:
        res = {'check', False}
        return jsonify(res)

    res = []
    for item in items:
        res.append(item[0])
    return jsonify(res)


@app.route('/getdeliverblereq',methods=['GET'])
def get_portfoliorequirement():
    username=request.args.get('username')
    coursename=request.args.get('coursename')
    items = query_factory.get_portfoliorequirement(username,coursename)
    print(username,coursename)
    print(items)
    if items == False:
        res ={'check',False}
        return jsonify(res)

    res = []
    for item in items:
        req_dict = {'name': item[0], 'id': item[1]}
        res.append(req_dict)
    return jsonify(res)

@app.route('/courses', methods=['GET', 'PUT', 'POST', 'DELETE'])
def courses():
    if request.method == 'GET':
        year = request.args.get('year')
        courses = query_factory.get_courses_by_year(year)
        courses_list = []
        for course in courses:
            course_dict = {'name': course[0], 'code': course[1], 'year': course[2]}
            staff_list = query_factory.get_course_staff(course[1])
            staff_members = []
            for staff_member in staff_list:
                staff_members.append(staff_member[0])
            course_dict['staff'] = staff_members
            courses_list.append(course_dict)
        return jsonify(courses_list)
    elif request.method == 'PUT':
        data = request.get_json()
        old_course_code = data.get('code')
        new_course_code = data.get('newCourse').get('code')
        new_course_name = data.get('newCourse').get('name')
        new_course_year = data.get('newCourse').get('year')
        new_course = Course(name=new_course_name, code=new_course_code, year=new_course_year)
        (is_successful, message) = query_factory.edit_course(old_course_code, new_course)
        response = {'is_successful': is_successful, 'message': message}
        return jsonify(response)
    elif request.method =='POST':
        data = request.get_json()
        new_course_code = data.get('newCourse').get('code')
        new_course_name = data.get('newCourse').get('name')
        new_course_year = data.get('newCourse').get('year')
        new_course = Course(name=new_course_name, code=new_course_code, year=new_course_year)
        (is_successful, message) = query_factory.add_course(new_course)
        response = {'is_successful': is_successful, 'message': message}
        return jsonify(response)
    elif request.method == 'DELETE':
        deleted_course_code = request.args.get('deletedCourseCode')
        (is_successful, message) = query_factory.delete_course(deleted_course_code)
        response = {'is_successful': is_successful, 'message': message}
        return jsonify(response)

@app.route('/users', methods=['POST'])
def users():
    if request.method == 'POST':
        data = request.get_json();
        user_type = data['user'].get('userType')
        username = data['user'].get('username')
        password = data['user'].get('password')
        email = data['user'].get('email')
        new_user = User(username=username, password=password, email=email, type=user_type)
        is_successful = query_factory.add_user(new_user)
        if not is_successful:
            response = {'is_successful': is_successful, 'message': 'Username already exists'}
            return jsonify(response)
        if user_type == 'STUDENT':
            name = data['user'].get('name')
            current_year = data['user'].get('currentYear')
            section_no = data['user'].get('sectionNo')
            bn = data['user'].get('bn')
            new_student = Student(name=name, current_year=current_year, section_no=section_no, bn=bn, username=username)
            is_successful = query_factory.add_student(new_student)
            if is_successful:
                id = query_factory.get_student_id(username)
                query_factory.enroll_students([id])
        elif user_type == 'STAFF':
            name = data['user'].get('name')
            department = data['user'].get('department')
            assigned_course_code = data['user'].get('course')
            new_staff_member = StaffMember(name=name, department=department, username=username)
            is_successful = query_factory.add_staff_member(new_staff_member)
            if is_successful and assigned_course_code != 'None':
                id = query_factory.get_staff_member_id(username)
                query_factory.assign_staff_members(ids=[id], course_code=assigned_course_code)
        else:
            pass
        if is_successful:
            message = 'User added successfully'
        else:
            message = 'User could not be added'
        response = {'is_successful': is_successful, 'message': message}
        return jsonify(response)

@app.route('/students', methods=['GET'])
def students():
    if request.method == 'GET':
        year = request.args.get('year')
        students = query_factory.get_students_by_year(year)
        students_list = []
        for student in students:
            student_dict = {'id': student[0], 'name':student[1]}
            students_list.append(student_dict)
        return jsonify(students_list)

@app.route('/semesters', methods=['POST', 'GET'])
def semesters():
    if request.method == 'POST':
        data = request.get_json()
        year = data.get('year')
        semester = data.get('semester')
        new_semester = Semester(semester=semester, year=year)
        is_successful = query_factory.add_semester(new_semester)
        if is_successful:
            msg = 'Semester created successfully.'
        else:
            msg = 'Semester could not be created.'
        response = {'is_successful': is_successful, 'message': msg}
        return jsonify(response)
    if request.method == 'GET':
        current_semester = query_factory.get_current_semester()
        semester = {'semester': current_semester.semester, 'year': current_semester.year}
        return jsonify(semester)

@app.route('/enroll', methods=['POST'])
def enroll():
    if request.method == 'POST':
        data = request.get_json()
        student_ids = data.get('ids')
        advanced_student_ids = data.get('advanced_student_ids')
        is_successful = query_factory.advance_students(advanced_student_ids)
        is_successful = is_successful and query_factory.enroll_students(student_ids)
        if is_successful:
            msg = 'Students enrolled successfully.'
        else:
            msg = 'Students could not be enrolled.'
        response = {'is_successful': is_successful, 'message': msg}
        return jsonify(response)

@app.route('/staff', methods=['GET'])
def staff():
    if request.method == 'GET':
        staff = query_factory.get_staff()
        staff_list = []
        for staff_member in staff:
            id = staff_member[0]
            name = staff_member[1]
            staff_dict = {'id': id, 'name': name}
            courses_list = query_factory.get_staff_member_last_semester_courses(id)
            courses = []
            for course in courses_list:
                courses.append(course[0])
            staff_dict['courses'] = courses
            staff_list.append(staff_dict)
        return jsonify(staff_list)

@app.route('/teach', methods=['POST'])
def teach():
    if request.method == 'POST':
        data = request.get_json()
        staff_members_ids = data.get('ids')
        course_code = data.get('courseCode')
        is_successful = query_factory.assign_staff_members(ids=staff_members_ids, course_code=course_code)
        if is_successful:
            msg = 'Staff members were assigned the course successfully.'
        else:
            msg = 'Staff members were not assigned the course.'
        response = {'is_successful': is_successful, 'message': msg}
        return jsonify(response)

@app.route('/requirements-statistics', methods=['GET'])
def requirements_statistics():
    if request.method == 'GET':
        reqID = request.args.get('reqID')
        requirement = query_factory.get_requirement(reqID)
        if requirement.type == 0:
            # Team requirement
            nTotal =  query_factory.get_requirement_number_of_teams(requirement.id)
        elif requirement.type == 1:
            # Student requirement
            nTotal = query_factory.get_requirement_number_of_students(requirement.course_code)

        (delivered_before_deadline, delivered_after_deadline) = query_factory.get_number_of_deliverables_deadline(requirement.id)
        (have_feedback, no_feedback) = query_factory.get_number_of_deliverables_feedback(requirement.id)

        response = {
            'requirement_type': requirement.type,
            'requirement_name': requirement.name,
            'delivered_before_deadline': delivered_before_deadline,
            'delivered_after_deadline': delivered_after_deadline,
            'have_feedback': have_feedback,
            'no_feedback': no_feedback,
            'n_total':nTotal
        }
        print(response)
        return jsonify(response)

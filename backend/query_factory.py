from database_manager import DatabaseManager
from models import User, Course, Student, StaffMember, Semester, Requirement
from typing import Optional
from psycopg2 import IntegrityError


class QueryFactory:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def initialize_connection(self, db_name: str, db_user: str, db_password) -> bool:
        connection_str: str = f"dbname='{db_name}' user='{db_user}' password='{db_password}'"
        response = self.db_manager.initialize_connection(connection_str)
        if response is None:
            return True  # Successful connection
        else:
            print(response)
            return False  # Unsuccessful connection


    def getCourses(self,usernamee):
        query: str = "select * from COURSE "\
                     "where CODE in (select ENROLL.COURSE_CODE  from ENROLL "\
                     f"where STUDENT_ID = (select ID from STUDENT  where USERNAME = '{usernamee}') "\
                     "and YEAR = (Select YEAR  from SEMESTER order by YEAR desc limit 1) "\
                     "and SEMESTER =(Select SEMESTER  from SEMESTER order by YEAR desc, SEMESTER desc limit 1)) "\

        response = self.db_manager.execute_query(query)
        print("//////getcourses////////////////////asdfasfsa////////////")
        print(query)
        return response

    def getRequirements(self,id):
        query: str = "select requirement.name,project.name,requirement.id from REQUIREMENT  " \
                    "left join project " \
                    "on project.id = requirement.project_id " \
                    "where requirement.id in (SELECT REQUIREMENT_ID from STD_ASSIGNED " \
                    f"where COURSE_CODE = '{id}' "\
                    "and YEAR = (Select YEAR  from SEMESTER order by YEAR desc limit 1) "\
                    "and SEMESTER = (Select SEMESTER  from SEMESTER order by YEAR desc, SEMESTER desc limit 1)) "\
                    "order by project.id,requirement.id "
        response = self.db_manager.execute_query(query)
        print(response)
        return response

    def getReqById(self,reqid):
        query: str = "select REQUIREMENT.*,lower(membersNumber),upper(membersNumber), COURSE.name, PROJECT.name from REQUIREMENT " \
                    "join COURSE on COURSE.code = REQUIREMENT.COURSE_CODE "\
                    "left join PROJECT on PROJECT.ID = REQUIREMENT.PROJECT_ID "\
                    f"where REQUIREMENT.id = {reqid} "
        print(f"2y 5ra m3a 2l     {reqid}                   /n  ")
        response = self.db_manager.execute_query(query)
        print(response)
        return response

    def isInTeam(self,reqid,usernamee) ->bool:
        query: str = "SELECT STUDENT_ID FROM FORM_TEAM "\
                    "WHERE TEAM_ID IN (SELECT TEAM_ID FROM TEAM "\
                    f"WHERE REQUIREMENT_ID = {reqid} and YEAR = (Select YEAR  from SEMESTER order by YEAR desc limit 1) "\
				" and SEMESTER = (Select SEMESTER  from SEMESTER order by YEAR desc, SEMESTER desc limit 1)) "\
                    f"AND STUDENT_ID = (select ID from STUDENT  where USERNAME = '{usernamee}') "
        response = self.db_manager.execute_query(query)
        if response:
            print("////////// HE IS IN A TEAM//////////")
            return True
        else:
            print("////////// HE IS NOOOT A TEAM//////////")
            return False


    def getStudentsInTeamInfo(self,reqid,usernamee):
        query: str = "select student.NAME, student.SECTION_NUMBER , student.BENCH_NUMBER ,student.USERNAME, account.email from student "\
                    "join account on student.username = account.username "\
                    "where id in (select student_id from form_team "\
                    "where team_id = (SELECT team_ID FROM FORM_TEAM "\
                    "WHERE TEAM_ID IN (SELECT TEAM_ID FROM TEAM "\
                    f"WHERE REQUIREMENT_ID = {reqid}) "\
                    f"and student_id = (select ID from STUDENT  where USERNAME = '{usernamee}') )) "\
                    f"and student.id <> (select ID from STUDENT  where USERNAME = '{usernamee}') "
        response = self.db_manager.execute_query(query)
        print(response)
        return response

    def getTeamInfo(self,reqid,usernamee):
        query: str = "select name,team_number,team_id from team "\
                    "where team_id = (SELECT team_ID FROM FORM_TEAM "\
                    "WHERE TEAM_ID IN (SELECT TEAM_ID FROM TEAM "\
                    f"WHERE REQUIREMENT_ID = {reqid}) "\
                    f"and student_id = (select ID from STUDENT  where USERNAME = '{usernamee}')) "
        response = self.db_manager.execute_query(query)
        print("/////////////////////////team info")
        print(response)
        print(response)
        return response

    def getStudentsNotInTeam(self,reqid,usernamee):
        query:str = "select student.id, student.name from student, requirement "\
                    "where student.id not in (SELECT STUDENT_ID FROM FORM_TEAM "\
                    "WHERE TEAM_ID IN (SELECT TEAM_ID FROM TEAM "\
                    f"WHERE REQUIREMENT_ID = {reqid} "\
                    "and SEMESTER = (Select SEMESTER  from SEMESTER order by YEAR desc, SEMESTER desc limit 1) "\
                    "and YEAR = (Select YEAR  from SEMESTER order by YEAR desc limit 1))) "\
                    f"and requirement.id = {reqid} and requirement.type = 0  and student.id <> (select ID from STUDENT  where USERNAME = '{usernamee}') "

        response = self.db_manager.execute_query(query)
        print(response)
        return response

    def isTeamNoAvilabe(self,reqid,tmn)->bool:
        print(reqid)
        print(tmn)
        query:str = f"select team_number from team where team_number = {tmn} and team_number  in( "\
                    "select TEAM_NUMBER from team "\
                    f"where REQUIREMENT_ID  = {reqid}  "\
                    "and SEMESTER = (Select SEMESTER  from SEMESTER order by YEAR desc, SEMESTER desc limit 1) "\
                    "and YEAR = (Select YEAR  from SEMESTER order by YEAR desc limit 1)) "
        print(query)
        response = self.db_manager.execute_query(query)
        print(response)
        if len(response) == 0:
            print("////////// Team No is Avilabe//////////")
            return True
        else:
            print("////////// Team NO isNot Avilable//////////")
            return False



    def addTeam(self, courseCode, reqID, teamNumber, teamName):
        query: str = f"INSERT INTO TEAM(COURSE_CODE, REQUIREMENT_ID, TEAM_NUMBER, NAME, SEMESTER, YEAR)" \
                     f"VALUES ('{courseCode}',{reqID}, {teamNumber}, '{teamName}', " \
                     f"(Select SEMESTER  from SEMESTER order by YEAR desc, SEMESTER desc limit 1), " \
                     f"(Select YEAR  from SEMESTER order by YEAR desc limit 1) )"
        response = self.db_manager.execute_query_no_return(query)
        query: str = "SELECT LASTVAL()"
        teamID = self.db_manager.execute_query(query)
        if response is not None:
            return (False, teamID[0][0])
        else:
            return (True, teamID[0][0])

    def get_student_id(self, username):
        query: str = f"SELECT ID FROM STUDENT WHERE USERNAME = '{username}'"
        response = self.db_manager.execute_query(query)
        if type(response) == Exception:
            return None
        else:
            return response[0][0]

    def fillTeamMembers(self, teamID, studentIDs):
        query: str = """
            INSERT INTO FORM_TEAM(STUDENT_ID, TEAM_ID)
            SELECT S.ID, T.TEAM_ID FROM STUDENT S, TEAM T
            WHERE ID IN %s AND TEAM_ID = %s
        """
        data = (tuple(studentIDs), teamID)
        response = self.db_manager.execute_query_no_return(query, data)
        if response is not None:
            return False
        else:
            return True

    def deliverableShit(self,reqID,username,teamID):
        print("///////////////////////////deliverable shit")
        print(teamID)
        if teamID == None:
            print("///////////////////////////////////////////individual////////////////////")
            query: str = "select d.id, d.IS_PUBLIC, d.MATERIALS, d.FEEDBACK, d.FEEDBACK_STAFF_ID, s.NAME from deliverable as d "\
                    "left join staff_member as s "\
                    "on s.id = d.FEEDBACK_STAFF_ID "\
                    f"where d.requirement_id = {reqID} and  d.student_id = (SELECT ID FROM STUDENT WHERE USERNAME = '{username}')  "\
                    "and d.SEMESTER = (Select SEMESTER  from SEMESTER order by YEAR desc, SEMESTER desc limit 1) "\
                    "and d.year = (Select YEAR  from SEMESTER order by YEAR desc limit 1) "

        else:
            print("///////////////////////////teatmtmtmtmtm////////////////////////////////")
            query: str = "select d.id, d.IS_PUBLIC, d.MATERIALS, d.FEEDBACK, d.FEEDBACK_STAFF_ID, s.NAME, s.CONTACT_INFO, s.OFFICE_HOURS from deliverable as d "\
                    "left join staff_member as s "\
                    "on s.id = d.FEEDBACK_STAFF_ID "\
                    "where  "\
                    f"d.requirement_id = {reqID} and d.team_id = {teamID} "\
                    "and d.SEMESTER = (Select SEMESTER  from SEMESTER order by YEAR desc, SEMESTER desc limit 1) "\
                    "and d.year = (Select YEAR  from SEMESTER order by YEAR desc limit 1) "

        response = self.db_manager.execute_query(query)
        print(response)
        if response == None:
            print("///////////////////////////////////////a7a//////////////////////")
        else:
            print("//////////////////////////////////////msh a7a 2we////////////////////////////////////")
        return response

    def adddeliverable(self,req_id,cCode,materials,delivery_time,tmID,username):
        if tmID == None:
            query:str = "insert into deliverable (REQUIREMENT_ID, COURSE_CODE, IS_PUBLIC, MATERIALS, DELIVERY_TIME, STUDENT_ID,year,SEMESTER) "\
                        f"values({req_id},'{cCode}',false,'{materials}', '{delivery_time}', (SELECT ID FROM STUDENT WHERE USERNAME = '{username}'), (Select YEAR  from SEMESTER order by YEAR desc limit 1), (Select SEMESTER  from SEMESTER order by YEAR desc, SEMESTER desc limit 1) ) "
        else:
            query:str = "insert into deliverable (REQUIREMENT_ID, COURSE_CODE, IS_PUBLIC, MATERIALS, DELIVERY_TIME, TEAM_ID,year,SEMESTER) "\
                        f"values({req_id},'{cCode}',false,'{materials}', '{delivery_time}', {tmID} ,(Select YEAR  from SEMESTER order by YEAR desc limit 1), (Select SEMESTER  from SEMESTER order by YEAR desc, SEMESTER desc limit 1)) "
        print("//////////////////adddeliverabel")
        print(query)
        response = self.db_manager.execute_query_no_return(query)
        if response is not None:
            return False
        else:
            return True

    def getstaffCourses(self,username):
        query:str = "select t.course_code, c.name from teach as t "\
                    "join course as c  "\
                    "on t.COURSE_CODE = c.code "\
                    f"where t.STAFF_MEMBER_ID = (select id from staff_member where username = '{username}') "\
                    "and t.SEMESTER = (Select SEMESTER  from SEMESTER order by YEAR desc, SEMESTER desc limit 1) "\
                    "and t.year = (Select YEAR  from SEMESTER order by YEAR desc limit 1) "

        response = self.db_manager.execute_query(query)
        return response

    def getreqbyCourseCode(self,cCode):
        query:str = "select r.id, r.name, p.name,p.id from requirement as r "\
                    "left join project as p on p.id = r.project_id "\
                    f"where r.course_code = '{cCode}' "\
                    "and r.id in(select requirement_id from std_assigned where year = (Select YEAR  from SEMESTER order by YEAR desc limit 1) "\
                    "and SEMESTER = (Select SEMESTER  from SEMESTER order by YEAR desc, SEMESTER desc limit 1)) "\
                    "order by p.id,r.id "
        response1 = self.db_manager.execute_query(query)
        query2:str = f"select name, id from project where course_code = '{cCode}'"
        response2 = self.db_manager.execute_query(query2)
        print("//////////////////////////////////////////////////////////////////////////////////////////")
        print(response1)
        print(response2)
        response = {}
        response["RDATA"] = response1
        response["PData"] = response2
        print(response)
        return response

    def addnewReqByStaff_member(self,insertionType,cCode,ProjectID,ProjectName,ProjectDocument,Name,DeadLine,addMaterials,document,type,minNumber,maxNumber):
        if insertionType == 3:
            if type == 1:
                minNumber = 0
                maxNumber = 0
            query:str = "insert into requirement(course_code,name,deadline,additional_materials,document,type,membersnumber) "\
                        f"values ('{cCode}','{Name}','{DeadLine}','{addMaterials}','{document}',{type},'[{minNumber},{maxNumber}]')"
            response = self.db_manager.execute_query_no_return(query)
            print(query)
            if response is not None:
                return False
            else:
                return True
        if insertionType == 1:
            if type == 1:
                minNumber = 0
                maxNumber = 0
            query1:str = "insert into project (course_code,name,document) "\
                        f"values ('{cCode}','{ProjectName}','{ProjectDocument}') "
            self.db_manager.execute_query_no_return(query1)
            query2:str = f"select id from project where course_code = '{cCode}' order by id desc limit  1"
            projnewID = self.db_manager.execute_query(query2)
            print(projnewID)
            query:str = "insert into requirement(course_code,project_id,name,deadline,additional_materials,document,type,membersnumber) "\
                        f"values ('{cCode}',{projnewID[0][0]},'{Name}','{DeadLine}','{addMaterials}','{document}',{type},'[{minNumber},{maxNumber}]')"
            response = self.db_manager.execute_query_no_return(query)
            if response is not None:
                return False
            else:
                return True
        if insertionType == 2:
            if type == 1:
                minNumber = 0
                maxNumber = 0
            query:str = "insert into requirement(course_code,project_id,name,deadline,additional_materials,document,type,membersnumber) "\
                        f"values ('{cCode}',{ProjectID},'{Name}','{DeadLine}','{addMaterials}','{document}',{type},'[{minNumber},{maxNumber}]')"

            print(query)
            response = self.db_manager.execute_query_no_return(query)
            if response is not None:
                return False
            else:
                return True


    def getUnassignedRequirements(self,cCode):
        query:str = "select r.name,r.id, p.name from requirement as r "\
                    "left join project as p "\
                    "on p.id = r.project_id "\
                    f"where r.id not in (select requirement_id from std_assigned where COURSE_CODE= '{cCode}' "\
                    "and year = (Select YEAR  from SEMESTER order by YEAR desc limit 1) "\
                    "and SEMESTER = (Select SEMESTER  from SEMESTER order by YEAR desc, SEMESTER desc limit 1)) "\
                    f"and r.course_code = '{cCode}' "
        response = self.db_manager.execute_query(query)
        print("////////////////////////////////////////////////////////////////////////")
        print(response)
        print("////////////////////////////////////////////////////////////////////////")
        print("////////////////////////////////////////////////////////////////////////")
        print(cCode)
        print("////////////////////////////////////////////////////////////////////////")
        return response

    def assignReqbyStaff(self,cCode,reqID):
        query:str = "insert into std_assigned "\
                    f"values ('{cCode}',{reqID},(Select YEAR  from SEMESTER order by YEAR desc limit 1),(Select SEMESTER  from SEMESTER order by YEAR desc, SEMESTER desc limit 1)) "

        response = self.db_manager.execute_query_no_return(query)
        if response is not None:
            return False
        else:
            query2:str = "select e.student_id from std_assigned as s "\
            "join enroll as e "\
            "on e.course_code = s.course_code "\
            f"where s.requirement_id = {reqID} "\
            "and e.SEMESTER = (SELECT SEMESTER FROM SEMESTER ORDER BY YEAR DESC, SEMESTER DESC LIMIT 1) "\
            "and e.YEAR = (SELECT YEAR FROM SEMESTER ORDER BY YEAR DESC LIMIT 1) "\
            "and s.SEMESTER = (SELECT SEMESTER FROM SEMESTER ORDER BY YEAR DESC, SEMESTER DESC LIMIT 1) "\
            "and s.YEAR = (SELECT YEAR FROM SEMESTER ORDER BY YEAR DESC LIMIT 1) "
            response1 = self.db_manager.execute_query(query2)
            data = []
            for x in response1:
                data.append(x[0])
            response3 =  self.get_requirement(reqID)
            name = response3.name
            msg: str = f"Requirement '{name}' was assigned for this semester"
            self.INSERT_NOTIFICATIONS(data,msg)
            return True

    def updateReqbyStaff(self,reqID,name,deadline,addMaterials,document):
        response3 =  self.get_requirement(reqID)
        name2 = response3.name
        query:str = "update requirement "\
                    f"set name='{name}', DEADLINE='{deadline}', ADDITIONAL_MATERIALS = '{addMaterials}', DOCUMENT ='{document}' "\
                    f"where id = {reqID} "
        response = self.db_manager.execute_query_no_return(query)
        if response is not None:
            return False
        else:
            query2:str = "select e.student_id from std_assigned as s "\
            "join enroll as e "\
            "on e.course_code = s.course_code "\
            f"where s.requirement_id = {reqID} "\
            "and e.SEMESTER = (SELECT SEMESTER FROM SEMESTER ORDER BY YEAR DESC, SEMESTER DESC LIMIT 1) "\
            "and e.YEAR = (SELECT YEAR FROM SEMESTER ORDER BY YEAR DESC LIMIT 1) "\
            "and s.SEMESTER = (SELECT SEMESTER FROM SEMESTER ORDER BY YEAR DESC, SEMESTER DESC LIMIT 1) "\
            "and s.YEAR = (SELECT YEAR FROM SEMESTER ORDER BY YEAR DESC LIMIT 1) "
            response1 = self.db_manager.execute_query(query2)
            data = []
            for x in response1:
                data.append(x[0])

            msg: str = f"Requirement '{name2}' was updated"
            self.INSERT_NOTIFICATIONS(data,msg)
            return True

    def getDeliverAblesbyStaff(self,reqID,cCode):
        query:str = "select d.*,t.name,s.name from deliverable as d "\
                    "left join team as t on d.team_id = t.team_id "\
                    "left join student as s on s.id = d.student_id "\
                    f"where   d.REQUIREMENT_ID = {reqID} and d.COURSE_CODE = '{cCode}' and "\
                    "d.YEAR = (Select YEAR  from SEMESTER order by YEAR desc limit 1) "\
                    "and d.SEMESTER = (Select SEMESTER  from SEMESTER order by YEAR desc, SEMESTER desc limit 1) "
        response = self.db_manager.execute_query(query)
        print("///////////////////////get all deliverables")
        print(response)
        return response
    def addFeedbackbyStadd(self,deliverableID,deliverableData,staffusername):
        query:str = "update deliverable "\
                    f"set FEEDBACK = '{deliverableData}', FEEDBACK_STAFF_ID = (select id from staff_member where username = '{staffusername}') "\
                    f"where id  = {deliverableID} "
        response = self.db_manager.execute_query_no_return(query)
        if response is not None:
            return False
        else:
            return True
    def getTeamsINRequirement(self,reqID,cCode):
        query:str = "select TEAM_ID,TEAM_NUMBER ,NAME from team "\
                    f"where REQUIREMENT_ID = {reqID} and COURSE_CODE = '{cCode}' "\
                    "and YEAR = (Select YEAR  from SEMESTER order by YEAR desc limit 1) "\
                    "and SEMESTER = (Select SEMESTER  from SEMESTER order by YEAR desc, SEMESTER desc limit 1) "
        response = self.db_manager.execute_query(query)
        print("///////////////////////get all teamssss")
        print(response)
        return response

    def deleteTeam(self,teamID):
        print("///////////////////////////////////////delete")
        query:str = f"DELETE FROM team WHERE TEAM_ID = {teamID} "
        response = self.db_manager.execute_query_no_return(query)
        if response is not None:
            return False
        else:
            return True

    def unassignReqbyStaff(self,reqID,cCode):
        query2:str = "select e.student_id from std_assigned as s "\
        "join enroll as e "\
        "on e.course_code = s.course_code "\
        f"where s.requirement_id = {reqID} "\
        "and e.SEMESTER = (SELECT SEMESTER FROM SEMESTER ORDER BY YEAR DESC, SEMESTER DESC LIMIT 1) "\
        "and e.YEAR = (SELECT YEAR FROM SEMESTER ORDER BY YEAR DESC LIMIT 1) "\
        "and s.SEMESTER = (SELECT SEMESTER FROM SEMESTER ORDER BY YEAR DESC, SEMESTER DESC LIMIT 1) "\
        "and s.YEAR = (SELECT YEAR FROM SEMESTER ORDER BY YEAR DESC LIMIT 1) "
        response1 = self.db_manager.execute_query(query2)
        data = []
        for x in response1:
            data.append(x[0])
        query:str = f"DELETE FROM STD_ASSIGNED  WHERE REQUIREMENT_ID={reqID} and COURSE_CODE='{cCode}'  "\
                    "and YEAR = (Select YEAR  from SEMESTER order by YEAR desc limit 1) "\
                    "and SEMESTER = (Select SEMESTER  from SEMESTER order by YEAR desc, SEMESTER desc limit 1)"
        response = self.db_manager.execute_query_no_return(query)
        if response is not None:
            return False
        else:

            response3 =  self.get_requirement(reqID)
            name = response3.name
            msg: str = f"Requirement '{name}' was unassigned for the semester"
            self.INSERT_NOTIFICATIONS(data,msg)
            return True
    def deleteReqbyStaff(self,reqID):
        query:str =f"Delete from REQUIREMENT where ID = {reqID}"
        response = self.db_manager.execute_query_no_return(query)
        print(query)
        if response is not None:
            return False
        else:
            return True

    def deleteDeliverable(self,delivID):
        query:str =f"Delete from DELIVERABLE  where ID = {delivID}"
        response = self.db_manager.execute_query_no_return(query)
        print(query)
        if response is not None:
            return False
        else:
            return True

    def is_user(self, user: User) -> Optional[bool]:
        print(user.username, user.password)
        query: str = f"select * from account where username='{user.username}'" \
                     f"and password='{user.password}'"

        response = self.db_manager.execute_query(query)
        if type(response) == Exception:
            return None
        elif response:
            return response
        else:
            return False

    def avi_email(self, user: User) -> Optional[bool]:
        query: str = f"select * from account where email='{user.email}'"
        response = self.db_manager.execute_query(query)
        if type(response) == Exception:
            return None
        elif response:
            return True
        else:
            return False

    def update_password(self, user: User):
        query: str = f"UPDATE account SET password='{user.password}'" \
                     f"WHERE email='{user.email}'"
        response = self.db_manager.execute_query_no_return(query)
        if type(response) == Exception:
            return None
        else:
            return True

    def Get_ALL(self, user: User):
        print(user.username, f"ely gay mn el database")
        query: str = f"select * from account where username='{user.username}'"
        response = self.db_manager.execute_query(query)
        if type(response) == Exception:
            return None
        elif response:
            return response
        else:
            return False

    def update_User(self, user: User, oldusername):
        print("in database")
        print(user.username)
        print(user.password)
        print(user.email)
        print(oldusername)
        query: str = f"UPDATE account SET password='{user.password}',username='{user.username}', email='{user.email}'" \
                     f"WHERE username='{oldusername}'"
        response = self.db_manager.execute_query_no_return(query)
        if type(response) == Exception:
            return False
        else:
            return True

    def GET_NOTIFICATIONS(self, username):
        query: str = f"select n.message , n.notification_id from notification n join user_notification u " \
                     f"on n.notification_id = u.notification_id where username='{username}'"

        response = self.db_manager.execute_query(query)
        if type(response) == Exception:
            return None
        elif response:
            return response
        else:
            return False

    def INSERT_NOTIFICATIONS(self, student_ids, message):
        query: str = f"insert INTO notification(message) values" \
                     f"('{message}');"
        response = self.db_manager.execute_query_no_return(query)
        if type(response) == Exception:
            return None
        else:
            query = "SELECT LASTVAL()"
            notification_id = self.db_manager.execute_query(query)
            notification_id = notification_id[0][0]
            query = """
                INSERT INTO USER_NOTIFICATION(USERNAME, NOTIFICATION_ID)
                SELECT S.USERNAME, NOTIFICATION_ID FROM STUDENT S, NOTIFICATION WHERE ID IN %s AND NOTIFICATION_ID = %s
            """
            data = (tuple(student_ids), notification_id)
            response = self.db_manager.execute_query_no_return(query, data)
            if response is None:
                return True
            else:
                return False


    def Delete_NOTIFICATIONS(self, username, id):
        query: str = f"delete from user_notification where username='{username}' and  notification_id ='{id}' ;"
        response = self.db_manager.execute_query_no_return(query)
        if type(response) == Exception:
            return None
        else:
            return True

    def get_portfoliocourses(self,username):
        query: str = f"SELECT distinct c.name FROM deliverable as d " \
                     f"join course as c " \
                     f"on c.code = d.course_code " \
                      f"where (d.student_id = (select id from student where username='{username}'))  or (d.team_id in (select team_id from form_team where student_id =(select id from student where username='{username}'))) "
        response = self.db_manager.execute_query(query)
        print(response)
        if type(response) == Exception:
            return None
        elif response:
            return response
        else:
            return False

    def get_portfoliorequirement(self,username,coursename):
        query:str=f"select r.name,r.id from deliverable d "\
                  f"join requirement r on r.id = d.requirement_id "\
                  f"join course c on c.code = d.course_code "\
                  f"where c.name = '{coursename}' and (d.student_id = (select id from student where username='{username}')) "\
                  f"					   union "\
                  f"select r.name,r.id from deliverable d "\
                  f"join requirement r on r.id = d.requirement_id "\
                  f"join course c on c.code = d.course_code "\
                  f"where c.name = '{coursename}' and (d.team_id in (select team_id from form_team where student_id =(select id from student where username='{username}'))) "
        print(username)
        response = self.db_manager.execute_query(query)
        print
        if type(response) == Exception:
            return None
        elif response:
            return response
        else:
            return False



    def get_portfolio(self, username,id):
        query: str = f"SELECT c.name,p.name,r.name, d.materials,r.type,t.name, d.feedback,s.semester,s.year	FROM deliverable as d " \
                     f"join course as c " \
                     f"on c.code = d.course_code " \
                     f"join requirement as r " \
                     f"on r.id=d.requirement_id " \
                     f"left join project as p " \
                     f"on p.id=r.project_id " \
                     f"left join team as t " \
                     f"on d.team_id=t.team_id " \
                     f"join std_assigned as s " \
                     f"on d.requirement_id=s.requirement_id " \
                     f"where d.requirement_id = {id} and " \
                     f"((d.student_id = (select id from student where username='{username}')) " \
                     f" or (d.team_id in (select team_id from form_team where student_id =(select id from student where username='{username}')))) " \
                     f"order by c.code,p.id,r.id ;"
        response = self.db_manager.execute_query(query)
        print(response)
        if type(response) == Exception:
            return None
        elif response:
            return response
        else:
            return False

    def get_students_by_year(self, year: int):
        query: str = f"SELECT ID, NAME FROM STUDENT WHERE CURRENT_YEAR = {year}"
        response = self.db_manager.execute_query(query)
        if type(response) == Exception:
            return None
        else:
            return response

    def get_courses_by_year(self, year: int):
        query: str = f"SELECT NAME, CODE, YEAR FROM COURSE WHERE YEAR = {year}"
        response = self.db_manager.execute_query(query)
        if type(response) == Exception:
            return None
        else:
            return response

    def edit_course(self, code: str, new_course:Course):
        query: str = f"UPDATE COURSE SET CODE = '{new_course.code}', NAME = '{new_course.name}', YEAR={new_course.year} " \
                     f"WHERE CODE = '{code}'"
        response = self.db_manager.execute_query_no_return(query)
        if type(response) == IntegrityError :
            return (False,"Course code already exists.")
        else:
            return (True,"Course modified successfully.")

    def add_course(self, new_course:Course):
        query: str = f"INSERT INTO COURSE(NAME, CODE, YEAR) VALUES('{new_course.name}','{new_course.code}',{new_course.year})"
        response = self.db_manager.execute_query_no_return(query)
        if type(response) == IntegrityError :
            return (False,"Course code already exists.")
        else:
            return (True,"Course added successfully.")

    def delete_course(self, code: str):
        query: str = f"DELETE FROM COURSE WHERE CODE = '{code}'"
        response = self.db_manager.execute_query_no_return(query)
        if type(response) == IntegrityError:
            return (False, "Course could not be deleted; one or more of its requirements where fulfilled by students.")
        else:
            return (True, "Course deleted successfully.")

    def get_course_staff(self, course_code: str):
        query: str = f"SELECT S.NAME FROM TEACH T JOIN STAFF_MEMBER S ON S.ID = T.STAFF_MEMBER_ID " \
                     f"WHERE T.COURSE_CODE = '{course_code}' AND SEMESTER = "\
                     f"(SELECT SEMESTER FROM SEMESTER ORDER BY YEAR DESC, SEMESTER DESC LIMIT 1)" \
                     f"AND YEAR = (SELECT YEAR FROM SEMESTER ORDER BY YEAR DESC LIMIT 1);"
        response = self.db_manager.execute_query(query)
        if type(response) == Exception:
            return None
        else:
            return response

    def add_user(self, user: User):
        query: str = f"INSERT INTO ACCOUNT(USERNAME, PASSWORD, EMAIL, USER_TYPE) VALUES " \
                     f"('{user.username}', '{user.password}', '{user.email}', '{user.type}')"
        response = self.db_manager.execute_query_no_return(query)
        if type(response) == IntegrityError:
            return False
        else:
            return True

    def add_student(self, student: Student):
        query: str = f"INSERT INTO STUDENT(NAME, CURRENT_YEAR, SECTION_NUMBER, BENCH_NUMBER, USERNAME) VALUES " \
                     f"('{student.name}', '{student.current_year}', '{student.section_no}', '{student.bn}', '{student.username}')"
        response = self.db_manager.execute_query_no_return(query)
        print(response)
        if type(response) == Exception:
            return False
        else:
            return True

    def add_staff_member(self, staff_member: StaffMember):
        query: str = f"INSERT INTO STAFF_MEMBER(NAME, DEPARTMENT, USERNAME) VALUES " \
                     f"('{staff_member.name}', '{staff_member.department}', '{staff_member.username}')"
        response = self.db_manager.execute_query_no_return(query)
        if type(response) == Exception:
            return False
        else:
            return True

    def add_semester(self, semester: Semester):
        query: str = f"INSERT INTO SEMESTER(SEMESTER, YEAR) VALUES " \
                     f"('{semester.semester}', {semester.year})"
        response = self.db_manager.execute_query_no_return(query)
        if type(response) == IntegrityError:
            return False
        else:
            return True

    def get_current_semester(self):
        query: str = f"SELECT SEMESTER, YEAR FROM SEMESTER WHERE " \
                     f"SEMESTER = "\
                     f"(SELECT SEMESTER FROM SEMESTER ORDER BY YEAR DESC, SEMESTER DESC LIMIT 1)" \
                     f"AND YEAR = (SELECT YEAR FROM SEMESTER ORDER BY YEAR DESC LIMIT 1)"
        response = self.db_manager.execute_query(query)
        [semester] = response
        current_semester = Semester(semester=semester[0], year=semester[1])
        if type(response) == Exception:
            return None
        else:
            return current_semester

    def advance_students(self, ids):
        query: str = "UPDATE STUDENT SET CURRENT_YEAR = CURRENT_YEAR + 1 WHERE ID IN %s"
        data = (tuple(ids),)
        response = self.db_manager.execute_query_no_return(query, data)
        if response is not None:
            return False
        else:
            return True

    def enroll_students(self, ids):
        query: str = """
            INSERT INTO ENROLL(STUDENT_ID, COURSE_CODE, SEMESTER, YEAR)
            SELECT * FROM
                (SELECT S.ID, C.CODe
                FROM STUDENT S
                JOIN COURSE C ON S.CURRENT_YEAR = C.YEAR
                WHERE S.ID IN %s) TEMP, SEMESTER
                WHERE SEMESTER = (SELECT SEMESTER FROM SEMESTER ORDER BY YEAR DESC, SEMESTER DESC LIMIT 1)
                AND YEAR = (SELECT YEAR FROM SEMESTER ORDER BY YEAR DESC LIMIT 1)
        """
        data = (tuple(ids),)
        response = self.db_manager.execute_query_no_return(query, data)
        if response is not None:
            return False
        else:
            return True

    def get_student_id(self, username):
        query: str = f"SELECT ID FROM STUDENT WHERE USERNAME = '{username}'"
        response = self.db_manager.execute_query(query)
        if type(response) == Exception:
            return None
        else:
            return response[0][0]

    def get_staff_member_id(self, username):
        query: str = f"SELECT ID FROM STAFF_MEMBER WHERE USERNAME = '{username}'"
        response = self.db_manager.execute_query(query)
        if type(response) == Exception:
            return None
        else:
            return response[0][0]

    def get_staff(self):
        query: str = "SELECT ID, NAME FROM STAFF_MEMBER"
        response = self.db_manager.execute_query(query)
        if type(response) == Exception:
            return None
        else:
            return response

    def get_staff_member_last_semester_courses(self, id):
        # Returns the courses of the LAST semester
        query: str = f"SELECT COURSE_CODE FROM TEACH WHERE STAFF_MEMBER_ID = {id} " \
                     f"AND SEMESTER = (SELECT SEMESTER FROM SEMESTER ORDER BY YEAR DESC, SEMESTER DESC LIMIT 1 OFFSET 1) " \
                     f"AND YEAR = (SELECT YEAR FROM SEMESTER ORDER BY YEAR DESC LIMIT 1 OFFSET 1)"
        response = self.db_manager.execute_query(query)
        if type(response) == Exception:
            return None
        else:
            return response

    def assign_staff_members(self, ids, course_code):
        # Assigns staff members to a specific course
        query: str = """
            INSERT INTO TEACH(STAFF_MEMBER_ID, COURSE_CODE, SEMESTER, YEAR)
            SELECT S.ID, C.CODE, SM.SEMESTER, SM.YEAR
            FROM STAFF_MEMBER S, COURSE C, SEMESTER SM
            WHERE C.CODE = %s AND S.ID IN %s
            AND SM.SEMESTER = (SELECT SEMESTER FROM SEMESTER ORDER BY YEAR DESC, SEMESTER DESC LIMIT 1)
            AND SM.YEAR = (SELECT YEAR FROM SEMESTER ORDER BY YEAR DESC LIMIT 1)
            """
        data = (course_code, tuple(ids))
        response = self.db_manager.execute_query_no_return(query, data)
        if response is not None:
            return False
        else:
            return True

    def get_requirement(self, reqID):
        query: str = f"SELECT * FROM REQUIREMENT WHERE ID = {reqID}"
        print(query)
        response = self.db_manager.execute_query(query)
        print('REQUIREMENT::')
        print(response)
        if type(response) == Exception:
            return None
        else:
            return Requirement(id=response[0][0],
                               course_code=response[0][1],
                               project_id=response[0][2],
                               name=response[0][3],
                               deadline=response[0][4],
                               additional_materials=response[0][5],
                               document=response[0][6],
                               type=response[0][7],
                               members_number=response[0][8])

    def get_requirement_number_of_teams(self, reqID):
        query: str = f"SELECT COUNT(*) FROM TEAM WHERE REQUIREMENT_ID = {reqID}"  \
                     f"AND SEMESTER = (SELECT SEMESTER FROM SEMESTER ORDER BY YEAR DESC, SEMESTER DESC LIMIT 1) " \
                     f"AND YEAR = (SELECT YEAR FROM SEMESTER ORDER BY YEAR DESC LIMIT 1)"
        response = self.db_manager.execute_query(query)
        print('NUMBER OF TEAMS::')
        print(response)
        if type(response) == Exception:
            return None
        else:
            return response[0]

    def get_requirement_number_of_students(self, course_code):
        query: str = f"SELECT COUNT(*) FROM ENROLL WHERE COURSE_CODE = '{course_code}'"  \
                     f"AND SEMESTER = (SELECT SEMESTER FROM SEMESTER ORDER BY YEAR DESC, SEMESTER DESC LIMIT 1) " \
                     f"AND YEAR = (SELECT YEAR FROM SEMESTER ORDER BY YEAR DESC LIMIT 1)"
        response = self.db_manager.execute_query(query)
        print('NUMBER OF STUDENTS::')
        print(response)
        if type(response) == Exception:
            return None
        else:
            return response[0]

    def get_number_of_deliverables_deadline(self, reqID):
        query: str = f"SELECT COUNT(*) FROM DELIVERABLE WHERE REQUIREMENT_ID = {reqID} " \
                     f"AND SEMESTER = (SELECT SEMESTER FROM SEMESTER ORDER BY YEAR DESC, SEMESTER DESC LIMIT 1) " \
                     f"AND YEAR = (SELECT YEAR FROM SEMESTER ORDER BY YEAR DESC LIMIT 1)"
        response = self.db_manager.execute_query(query)
        print('TOTAL DELIVERED::')
        print(response)
        if type(response) == Exception:
            return None
        else:
            total_delivered = response[0][0]

        query: str = f"SELECT COUNT(*) FROM DELIVERABLE D JOIN REQUIREMENT R ON R.ID = D.REQUIREMENT_ID "  \
                     f"WHERE DELIVERY_TIME <= DEADLINE AND REQUIREMENT_ID = {reqID} " \
                     f"AND SEMESTER = (SELECT SEMESTER FROM SEMESTER ORDER BY YEAR DESC, SEMESTER DESC LIMIT 1) " \
                     f"AND YEAR = (SELECT YEAR FROM SEMESTER ORDER BY YEAR DESC LIMIT 1)"
        response = self.db_manager.execute_query(query)
        print('DELIVERED BEFORE DEADLINE::')
        print(response)
        if type(response) == Exception:
            return None
        else:
            delivered_before_deadline = response[0][0]
            delivered_after_deadline = total_delivered - delivered_before_deadline
            return (delivered_before_deadline, delivered_after_deadline)

    def get_number_of_deliverables_feedback(self, reqID):
        query: str = f"SELECT COUNT(*) FROM DELIVERABLE WHERE REQUIREMENT_ID = {reqID} " \
                     f"AND SEMESTER = (SELECT SEMESTER FROM SEMESTER ORDER BY YEAR DESC, SEMESTER DESC LIMIT 1) " \
                     f"AND YEAR = (SELECT YEAR FROM SEMESTER ORDER BY YEAR DESC LIMIT 1)"
        response = self.db_manager.execute_query(query)
        if type(response) == Exception:
            return None
        else:
            total_delivered = response[0][0]

        query: str = f"SELECT COUNT(*) FROM DELIVERABLE WHERE REQUIREMENT_ID = {reqID} " \
                     f"AND SEMESTER = (SELECT SEMESTER FROM SEMESTER ORDER BY YEAR DESC, SEMESTER DESC LIMIT 1) " \
                     f"AND YEAR = (SELECT YEAR FROM SEMESTER ORDER BY YEAR DESC LIMIT 1)" \
                     f"AND FEEDBACK IS NOT NULL"

        response = self.db_manager.execute_query(query)
        if type(response) == Exception:
            return None
        else:
            have_feedback = response[0][0]
            no_feedback = total_delivered - have_feedback
            return (have_feedback, no_feedback)

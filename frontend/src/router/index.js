import Vue from 'vue'
import Router from 'vue-router'
import LoginForm from '@/components/LoginForm'
import NavBar from '@/components/NavBar'
import StudentCourses from '@/components/courses/StudentCourses'
import studentReq from '@/components/courses/studentReq'
import staff1 from '@/components/courses/staff1'
import staff2 from '@/components/courses/staff2'
import NewPassword from '@/components/NewPassword'
import Account from '@/components/Account'
import Home from '@/components/Home'
import NotFound from '@/components/NotFound'
import AdminPanel from '@/components/admin/AdminPanel'
import AdminCourses from '@/components/admin/AdminCourses'
import AddUser from '@/components/admin/AddUser'
import EnrollStudents from '@/components/admin/new-semester/EnrollStudents'
import ChooseSemester from '@/components/admin/new-semester/ChooseSemester'
import AssignStaff from '@/components/admin/new-semester/AssignStaff'
import RequirementStatistics from '@/components/courses/RequirementStatistics'
import Portfolio from '@/components/Portfolio'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      components: {
        mainContent: LoginForm
      }
    },
    {
      path: '/course',
      name: 'Courses/Req',
      components: {
        navbar: NavBar,
        mainContent: StudentCourses
      }
    },
    {
      path: '/studentReq',
      name: 'std/Req',
      components: {
        navbar: NavBar,
        mainContent: studentReq
    }
  },
  {
    path: '/home',
    name: 'Home',
    components: {
      navbar: NavBar,
      mainContent: Home
    }
  },
  {
    path: '/staff1',
    name: 'staffCourserandreq1',
    components: {
      navbar: NavBar,
      mainContent: staff1
    }
  },
  {
    path: '/staff2',
    name: 'staffCourserandreq',
    components: {
      navbar: NavBar,
      mainContent: staff2
    }
  },
  {
      path: "/NewPassword",
      name: "NewPassword",
      components:{
        mainContent:NewPassword
      }
    },
    {
      path: "/Account",
      name: "Account",
      components:{
        navbar:NavBar,
        mainContent:Account
      }
    },
  {
    path: '/portfolio',
    name: 'Portfolio',
    components: {
      navbar:NavBar,
      mainContent:Portfolio
    }
  },
  {
      path:'/admin',
      name: 'Admin Panel',
      components: {
        mainContent:AdminPanel
      }
    },
    {
      path:'/admin/courses',
      name: 'Admin - Courses',
      components: {
        mainContent:AdminCourses
      }
    },
    {
      path:'/admin/add-user',
      name: 'Admin - Add User',
      components: {
        mainContent:AddUser
      }
    },
    {
      path:'/admin/new-semester/enroll-students',
      name: 'Admin - New Semester - Enroll Students',
      components: {
        mainContent:EnrollStudents
      }
    },
    {
      path:'/admin/new-semester/choose-semester',
      name: 'Admin - New Semester - Choose Semester',
      components: {
        mainContent:ChooseSemester
      }
    },
    {
      path:'/admin/new-semester/assign-staff',
      name: 'Admin - New Semester - Assign Staff',
      components: {
        mainContent:AssignStaff
      }
    },
    {
      path: '/requirement-statistics',
      name: 'Requirement Statistics',
      components: {
        navbar: NavBar,
        mainContent: RequirementStatistics
      }
    },
    {
      path:'*',
      components:{
      mainContent:NotFound
      }
    }
  ]
})

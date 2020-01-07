import json
import requests


headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
TryLogin = 'https://levnet.jct.ac.il/api/home/login.ashx?action=TryLogin'
LoadAnnouncements = 'https://levnet.jct.ac.il/api/common/announcements.ashx?action=LoadAnnouncements'
DownloadFile = 'https://levnet.jct.ac.il/api/common/announcements.ashx?action=DownloadFile&fileId='
def downloadAllNotpadesExist(folder, username, password):
    login_data = {'username':username,"password":password}
    with requests.Session() as s:
        url = TryLogin
        url2 = "https://levnet.jct.ac.il/api/student/testNotebooks.ashx?action=SearchQuery"
        url3 = "https://levnet.jct.ac.il/api/student/testNotebooks.ashx?action=DownloadNotebook&notebookId="
        url4 = "https://levnet.jct.ac.il//api/student/coursePartGrades.ashx?action=GetStudentCoursePartGrades"
        r = s.get(url, headers=headers)
        print(json.loads(r.content))
        r = s.post(url, data=login_data, headers=headers)
        print(json.loads(r.content))
        r = s.get(url2, headers=headers)
        print(json.loads(r.content))
        r = s.post(url2, data=login_data, headers=headers)
        for page in range(1,json.loads(r.content)["buttonsCount"]):
            r = s.post(url2, data={"selectedAcademicYear":None,"selectedSemester":None,"selectedTestTimeType":None,"current":page}, headers=headers)
            items = json.loads(r.content)['items']
            for i in items:
                r = s.post(url4, data={"actualCourseId":i["actualCourseID"]}, headers=headers)
                grade = "חסר"
                if(i["testTimeTypeName"] == "מועד א"):
                    grade = json.loads(r.content)["partGrades"][0]["gradeAName"]
                elif(i["testTimeTypeName"] == "מועד ב"):
                    grade = json.loads(r.content)["partGrades"][0]["gradeBName"]
                elif(i["testTimeTypeName"] == "מועד ג"):
                    grade = json.loads(r.content)["partGrades"][0]["gradeCName"]
                u = requests.get(url3+str(i["id"]), headers=headers, cookies=s.cookies, allow_redirects=True)
                file = open(folder + "/"+i["courseName"] +" "+ i["academicYearName"].replace('"',"") +" " + i["semesterName"] + i["testTimeTypeName"].replace("מועד","") +" " + str(grade)+".pdf","wb")
                print(folder + "/"+i["courseName"] +" "+ i["academicYearName"].replace('"',"") +" " + i["semesterName"] + i["testTimeTypeName"].replace("מועד","") +" " + str(grade))
                file.write(u.content)
                file.close()


        

downloadAllNotpadesExist("מחברות בחינה", "egoldshm", "-------")

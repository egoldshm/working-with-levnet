import json
import requests


headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
TryLogin = 'https://levnet.jct.ac.il/api/home/login.ashx?action=TryLogin'
LoadAnnouncements = 'https://levnet.jct.ac.il/api/common/announcements.ashx?action=LoadAnnouncements'
DownloadFile = 'https://levnet.jct.ac.il/api/common/announcements.ashx?action=DownloadFile&fileId='
def registerToCourses(username, password, courses):
    login_data = {'username':username,"password":password}
    with requests.Session() as s:
        url = TryLogin
        url2 = "https://levnet.jct.ac.il/api/student/buildSchedule.ashx?action=LoadDataForBuildScheduleStart"
        url3 = "https://levnet.jct.ac.il/Student/Schedule/CoursesScheduleNew.aspx"
        url4 = "https://levnet.jct.ac.il/api/student/buildSchedule.ashx?action=LoadData"
        url5 = "https://levnet.jct.ac.il/api/student/buildSchedule.ashx?action=LoadCoursesForTrack"
        r = s.get(url, headers=headers)
        print(json.loads(r.content))
        r = s.post(url, data=login_data, headers=headers)
        print(json.loads(r.content))
        r = s.get(url2, headers=headers)
        r = s.post(url2, data=login_data, headers=headers)
        result = json.loads(r.content)
        #if regitertion is close
        if(result["isBlocked"] or result["isCreationBlocked"] or result["semestersScheduleCreation"] == [] or result["success"] == False):
            return False
        #if open
        for i in courses:
            r = s.get(url5, headers=headers)
            result = json.loads(r.content)
            r = s.post(url5,data={"selectedTrack":33}, headers=headers)
            result = json.loads(r.content)
            print(result)
        
        

        

registerToCourses("egoldshm", "------",{32987:[1,11]})

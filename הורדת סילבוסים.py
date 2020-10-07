import json
from os import path

import requests

SEMESTER = 3  # a = 2, b = 3, elul = 0
YEAR = 5780
MACHON = 1  # lev = 1, tal = 2

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
TryLogin = 'https://levnet.jct.ac.il/api/home/login.ashx?action=TryLogin'
LoadActualCourses = 'https://levnet.jct.ac.il/api/common/actualCourses.ashx?action=LoadActualCourses'
DownloadFile = 'https://levnet.jct.ac.il/api/common/actualCourses.ashx?ActualCourseID={}&action=DownloadSyllabus'


def fromJson(r):
    return json.loads(r.content)


def downloadAllSilabuses(folder, username, password):
    login_data = {'username': username, "password": password}
    with requests.Session() as s:
        r = s.get(TryLogin, headers=headers)
        print(json.loads(r.content))
        r = s.post(TryLogin, data=login_data, headers=headers)
        print(json.loads(r.content))
        data_of_req = {"selectedAcademicYear": YEAR, "selectedSemester": SEMESTER, "selectedExtension": MACHON,
                       "selectedCategory": None, "freeSearch": None, "current": 1}
        r = s.post(LoadActualCourses, data=data_of_req, headers=headers)

        amount_of_pages = fromJson(r)["totalPages"]
        for page in range(1, amount_of_pages + 1):
            data_of_req["current"] = page
            r = s.post(LoadActualCourses, data=data_of_req, headers=headers)
            items = json.loads(r.content)['items']
            for i in items:
                id = str(i["id"])
                course_name = i["courseName"].replace('"',"").replace("'","").replace("-"," ").replace("/", "")
                file_name = "סילבוס של " + course_name + ".pdf"
                print(file_name)
                file_path = folder + "//" + file_name
                if not path.exists(file_path):
                    u = requests.get(DownloadFile.format(id), headers=headers, cookies=s.cookies, allow_redirects=True)
                    file = open(file_path, "wb")
                    print(file_path)
                    file.write(u.content)
                    file.close()


def main():
    downloadAllSilabuses("סילבוסים לסמסטר ב", "egoldshm", input("Enter password>\n"))


main()

import json
import requests
import sys

fileName = "ממוצעים.csv"
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 '
                  'Safari/537.36'}
url_try_login = 'https://levnet.jct.ac.il/api/home/login.ashx?action=TryLogin'
url_load_actual_course = "https://levnet.jct.ac.il/api/common/actualCourses.ashx?action=LoadActualCourse&ActualCourseID="
url_load_grades_charts = "https://levnet.jct.ac.il/api/student/GradesCharts.ashx?action=LoadData&ActualCourseID="
MAX = 35000


def get_all_grades_charts_to_file(username, password, start_point=1, end = MAX):
    login_data = {'username': username, "password": password}
    with requests.Session() as s:
        if start_point == 1:
            file = open(fileName, "w")
            file.write(",".join(["מספר קורס", "מס'", "שם קורס", "שנה", "סמסטר",
                                 "ממוצע כולל", "חציון העוברים",
                                 "ממוצע העוברים", "מספר העוברים", "מספר הסטודנטים",
                                 "0-59", "60-64", "65-69", "70-74",
                                 "75-79", "80-84", "85-89", "90-94", "95-100",
                                 "failedGrades", "passedGrades", "שם מחלקה", "נק",
                                 "קטגוריית הקורס", "ציון מינימלי"]) + "\n")
            file.close()
        r = s.get(url_try_login, headers=headers, verify=False)
        print(json.loads(r.content))
        r = s.post(url_try_login, data=login_data, headers=headers, verify=False)
        print(json.loads(r.content))
        str_to_save = ""
        for i in range(start_point, end):
            try:
                line = get_info_for_course(i, login_data, s)
                print(line)
                str_to_save += ",".join(line) + "\n"
            except:
                print(f"{i}\tERROR:\t{sys.exc_info()[0]}")
            finally:
                if i % 1000 == 0:
                    with open(fileName, 'a') as f:
                        f.write(str_to_save)
                        str_to_save = ""


def get_info_for_course(i, login_data, s):
    r = s.post(url_load_grades_charts + str(i), data=login_data, headers=headers, verify=False)
    r2 = s.post(url_load_actual_course + str(i), data=login_data, headers=headers, verify=False)
    result = json.loads(r.content)
    result2 = json.loads(r2.content)
    courseAverage = result["courseAverage"]
    grades = result["grades"]
    line = list(map(str, [i, result["courseFullNumber"], result["courseName"], result["academicYear"],
                          result["semester"],
                          courseAverage["totalCourseAverage"], courseAverage["passedCourseMedian"],
                          courseAverage["passedCourseAverage"], courseAverage["sumOfPassedStudents"],
                          courseAverage["sumOfStudents"],
                          grades["_0to59"], grades["_60to64"], grades["_65to69"],
                          grades["_70to74"],
                          grades["_75to79"], grades["_80to84"], grades["_85to89"],
                          grades["_90to94"], grades["_95to100"],
                          grades["failedGrades"], grades["passedGrades"],
                          result2["details"]["extensionName"], result2["details"]["credits"],
                          result2["details"]["courseCategoryName"], result2["details"]["minGrade"]]))
    return line


def main():
    password = input("Enter password>\n")
    num = input("Enter number to start with>")
    end_point = input("Enter number to start with>")
    if not end_point.isdigit():
        end_point = MAX
    get_all_grades_charts_to_file("egoldshm", password, int(num), int(end_point))


if __name__ == "__main__":
    main()

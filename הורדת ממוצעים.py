import json
import requests
import sys


fileName = "ממוצעים.csv"
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
TryLogin = 'https://levnet.jct.ac.il/api/home/login.ashx?action=TryLogin'

def getStat(folder, username, password):
    login_data = {'username':username,"password":password}
    ## wb = load_workbook("ממוצעים.xlsx")
    # Select First Worksheet
    ## ws = wb.worksheets[0]
    with requests.Session() as s:
        url = TryLogin
        file = open(fileName, "w")
        file.write(",".join(["מספר קורס","שם קורס","שנה","סמסטר",
                                 "ממוצע כולל", "חציון העוברים",
                                 "ממוצע העוברים", "מספר העוברים", "מספר הסטודנטים",
                                 "0-59", "60-64","65-69","70-74",
                               "75-79","80-84","85-89", "90-94","95-100",
                                 "failedGrades","passedGrades","שם מחלקה","נק",
                                 "קטגוריית הקורס","ציון מינימלי"]) + "\n")
        file.close()
        url2 = "https://levnet.jct.ac.il/Student/GradesCharts.aspx?ActualCourseID="
        url3 = "https://levnet.jct.ac.il/api/common/actualCourses.ashx?action=LoadActualCourse&ActualCourseID="
        url4 = "https://levnet.jct.ac.il/api/student/GradesCharts.ashx?action=LoadData&ActualCourseID="
        #r = s.get(url, headers=headers)
        #print(json.loads(r.content))
        r = s.post(url, data=login_data, headers=headers, verify = False)
        #print(json.loads(r.content))
        strToFile = ""
        for i in range(1,35000):
            url = url4 + str(i)
            ## r = s.get(url, headers=headers)
            r = s.post(url, data=login_data, headers=headers, verify = False)
            r2 = s.post(url3 + str(i), data=login_data, headers=headers, verify = False)
            try: 
                result = json.loads(r.content)
                result2 = json.loads(r2.content)
                
                print(str(i) +"\t"+ result["courseName"] + "\t" + result["academicYear"] + "\t" + result["semester"] +
                  "\tavg: " + str(result["courseAverage"]["totalCourseAverage"]) + "\tmed: " + str(result["courseAverage"]["passedCourseMedian"]))

                courseAverage = result["courseAverage"]
                grades = result["grades"]
                line = ",".join([str(i),result["courseFullNumber"],result["courseName"],result["academicYear"],result["semester"],
                                 str(courseAverage["totalCourseAverage"]), str(courseAverage["passedCourseMedian"]),
                                 str(courseAverage["passedCourseAverage"]), str(courseAverage["sumOfPassedStudents"]), str(courseAverage["sumOfStudents"]),
                                 str(grades["_0to59"]), str(grades["_60to64"]),str(grades["_65to69"]),str(grades["_70to74"]),
                               str(grades["_75to79"]),str(grades["_80to84"]),str(grades["_85to89"]), str(grades["_90to94"]),str(grades["_95to100"]),
                                 str(grades["failedGrades"]),str(grades["passedGrades"]),result2["details"]["extensionName"],str(result2["details"]["credits"]),
                                 result2["details"]["courseCategoryName"],str(result2["details"]["minGrade"])]) + "\n"
                strToFile = strToFile + line
                # ws.append([str(i),result["courseFullNumber"],result["courseName"],result["academicYear"],result["semester"],str(result["courseAverage"]["totalCourseAverage"]),
                #         str(result["courseAverage"]["passedCourseMedian"]), str(result["courseAverage"]["passedCourseAverage"]),str(grades["_0to59"]),
                #          str(grades["_60to64"]),str(grades["_65to69"]),str(grades["_70to74"]),
                #              str(grades["_75to79"]),str(grades["_80to84"]),str(grades["_85to89"]),
                #          str(grades["_90to94"]),str(grades["_95to100"])])
            except:
                print(f"{i}\tERROR:\t{sys.exc_info()[0]}")
            finally:
                if(i % 500 == 0):
                    with open(fileName,'a') as f:
                        f.write(strToFile)
                        strToFile = ""
            ## wb.save("ממוצעים.xlsx")
        

getStat("מחברות בחינה", "egoldshm", "058jabcc400")

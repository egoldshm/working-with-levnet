var HOURS_OF_TESTS = 3;

//Tools:
Date.prototype.addHours = function(h) {
  var new_val = new Date(this)
  new_val.setHours(this.getHours() + h);
  return new_val;
}

Date.prototype.f = function(h) {
  return new Date(this.toGMTString());
}

function getRangeV(str) {
  var sheet = SpreadsheetApp.getActiveSheet();
  return sheet.getRange(str).getValue()
}

//add to menu
function onOpen() {
  SpreadsheetApp.getUi().createMenu("מערכת").addItem("הוסף ליומן", "addToCal")
}

//get info about event and add to calendar every week
function addTestToCal(cal, name,  start) {
  var start_date = new Date(start);
  var end_date = start_date.addHours(HOURS_OF_TESTS);
  var x = cal.createEvent(name,
    start_date.f(),
    end_date.f());
}
function getTestsByUsernamePassword(username, password, year, semester) {
  var session = new Session(username, password)
  if(session.status == false)
    throw "username or password incorrect";
  var data2 = {
    'selectedAcademicYear': year,
    'selectedSemester': semester
  }
  session.send('https://levnet.jct.ac.il/api/student/Tests.ashx?action=LoadFilters', null);
  session.send('https://levnet.jct.ac.il/api/student/Tests.ashx?action=LoadTests', data2);
  Logger.log(session.result)
  return session.resultAsJson.items;
}
/*function getLessonsByUsernamePassword(username, password, year, semester) {
  // Make a POST request with a JSON payload.
  var data1 = {
    'username': username,
    'password': password
  };

  var options1 = {
    'method': 'post',
    'contentType': 'application/json',
    // Convert the JavaScript object to a JSON string.
    'payload': JSON.stringify(data1),
  };

  var result = UrlFetchApp.fetch('https://levnet.jct.ac.il/api/home/login.ashx?action=TryLogin', options1);
  var params = JSON.parse(result.getContentText());
  if (params.success == false) {
    return false;
  }

  var cookie = result.getAllHeaders()['Set-Cookie'];

  var header = {
    'Cookie': cookie
  };
  var data2 = {
    'selectedAcademicYear': year,
    'selectedSemester': semester
  }
  var options2 = {
    'method': 'post',
    'contentType': 'application/json',
    // Convert the JavaScript object to a JSON string.
    'payload': JSON.stringify(data2),
    "headers": header
  };


  var result2 = UrlFetchApp.fetch('https://levnet.jct.ac.il/api/student/schedule.ashx?action=LoadWeeklySchedule', options2);
  var cookie = result2.getAllHeaders()['Set-Cookie'];
  var header = {
    'Cookie': cookie
  };
  var options3 = {
    'method': 'post',
    'contentType': 'application/json',
    // Convert the JavaScript object to a JSON string.
    'payload': JSON.stringify(data2),
    "headers": header
  };

  Logger.log(result2.getContentText());


  var result3 = UrlFetchApp.fetch('https://levnet.jct.ac.il/api/student/schedule.ashx?action=LoadScheduleList', options3);

  Logger.log(result3.getContentText());
  var params = JSON.parse(result3.getContentText());

  return params.groupsWithMeetings;

}*/

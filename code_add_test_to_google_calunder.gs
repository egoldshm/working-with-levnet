///////////////////////////////////////
// Written by Eytan Goldshmidt in 5780 //
//       eitntt@gmail.com            //
///////////////////////////////////////

function clickThisFunction() {
  var name = getRangeV("name")
  var username = getRangeV("username"),
    password = getRangeV("password"),
    sem = getRangeV("sem"),
    year = getRangeV("year");
  var rangePassword = SpreadsheetApp.getActiveSheet().getRange("password");
  rangePassword.setBackground("#d9d2e9");
  if (password == "") {
    rangePassword.setBackground("red");
    Browser.msgBox("נא להזין סיסמה");
    return;

  }
  var cals = CalendarApp.getCalendarsByName(name).filter(function (item) {
    return item.isOwnedByMe()
  });
  var cal;
  if (cals.length == 0)
    cal = CalendarApp.createCalendar(name);
  else
    cal = cals[0];
  try {
    var tests = getTestsByUsernamePassword(username, password, year, sem);
    if (tests == false) {
      rangePassword.setBackground("red");
      Browser.msgBox("סיסמה שגויה");
      return;
    }
    for (var i in tests) {
      var test = tests[i];
      Logger.log(test);
      var moed = test.testTimeTypeName;
      var name = test.courseName + " (" + moed +")";
      var time = test.startDate;
      addTestToCal(cal, name, time);
    }
  } catch (ex) {
    var s = SpreadsheetApp.getActiveSheet();
    var n = s.getLastRow();
    s.getRange(n + 1, 1).setValue(ex);
    //var s = SpreadsheetApp.getActiveSheet();
    //s.getRange(s.getLastRow() + 1, 1).setValue(ex);
    clickThisFunction();
  }

}

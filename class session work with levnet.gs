var Session = function(username, password) {
        this.username = username;
        this.password = password;
        var data1 = {
            'username': username,
            'password': password
        };

        var options1 = {
            'method': 'post',
            'contentType': 'application/json',
            'payload': JSON.stringify(data1),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'
        };

        var result = UrlFetchApp.fetch('https://levnet.jct.ac.il/api/home/login.ashx?action=TryLogin', options1);
        var params = JSON.parse(result.getContentText());
        this.status = params.success;
        this.cookie = result.getAllHeaders()['Set-Cookie'];
        this.result = result;
        try {
            this.resultAsJson = JSON.parse(result.getContentText());
        } catch (e) {
            throw e;
            this.resultAsJson = false;
        }
    


    this.send = function(url, data) {
        var header = {
            'Cookie': this.cookie
        };
        var options = {
            'method': 'post',
            'contentType': 'application/json',
            'payload': JSON.stringify(data),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
            "headers": header
        };
        var result = UrlFetchApp.fetch(url, options);
        this.cookie = result.getAllHeaders()['Set-Cookie'];
        this.result = result.getContentText();
        try {
            this.resultAsJson = JSON.parse(result.getContentText());
        } catch (e) {
            throw e;
            this.resultAsJson = false;
        }

    }

}

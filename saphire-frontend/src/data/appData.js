
export const getStockData = (company, from, to) => {
    return massageData(searchStock(company, from, to));
    //return searchStock(company)
}

export const getStockNews = (company) => {
    return searchNews(company);
}

export const getWatchedStocksData = () => {
    return userStocks();
}

function userStocks() {
    var xmlHttp = new XMLHttpRequest();
    var token = localStorage.getItem("token");
    
    xmlHttp.open("POST", "http://127.0.0.1:8000/api/watchedList/", false);
    xmlHttp.setRequestHeader("Content-Type","application/json");
    xmlHttp.setRequestHeader("Authorization", "Token " + token);
    xmlHttp.send( null );

    if (xmlHttp.status === 200){
        var json = JSON.parse(xmlHttp.responseText);
        var data = [];
        var index = 0;

        for (var stock in json){
            var company = new Object;
            var priceHistory = [];
            var phIndex = 0;
            company["Ticker"] = json[stock][0]['company'];

            for (var item in json[stock]){
                priceHistory[phIndex] = json[stock][item]['close'];
                phIndex++;
            }
            company["PriceHistory"] = priceHistory;
            //company["Action"] = "delete";
            data[index] = company;
            index++;
        }
        return data;
    }
    
}

function searchStock(ticker, from, to) {
    var token = localStorage.getItem("token");
    console.log("token " + token);
    //var theUrl = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker + '&outputsize=full&apikey=23V86RX6LO5AUIX4';
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "POST", 'http://127.0.0.1:8000/api/stocks/stockRange/', false ); // false for synchronous request
    //xmlHttp.send( null );

    xmlHttp.setRequestHeader("Content-Type","application/json");
    xmlHttp.setRequestHeader("Authorization", "Token " + token);

    console.log(from);
    console.log(to);
    xmlHttp.send(JSON.stringify({ ticker: ticker, low_date: formatDate(from) , high_date: formatDate(to) }));
    var json = JSON.parse(xmlHttp.responseText);
    
    return json;
}

function massageData(obj) {
    var result = "[";

    for (var day in obj) {
        result += "{ \"Date\": \"\\/Date(" + new Date(obj[day]["date"]).getTime() + ")\\/\""
                + ",\n\"Close\": " + obj[day]["close"] 
                + ",\n\"Volume\": " + obj[day]["vol"] 
                + ",\n\"Open\": " + obj[day]["open"] 
                + ",\n\"High\": " + obj[day]["high"] 
                + ",\n\"Low\": " + obj[day]["low"] + "},\n";
    }
    result = result.trim();
    result = result.substring(0, result.length - 1); 
    result += "]";
    console.log(result)
    JSON.parse(result);
    console.log("success");
    return JSON.parse(result);
}

function searchNews(company) {
    var theUrl = 'http://newsapi.org/v2/everything?' +
                    'q=' + company + '&' +
                    'lannguage=en&' +
                    'sortBy=popularity&' +
                    'apiKey=cc333d1d3a694724853412ba412eab31';
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );

    var json = JSON.parse(xmlHttp.responseText);

    return json.articles;
}

function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) 
        month = '0' + month;
    if (day.length < 2) 
        day = '0' + day;

    return [year, month, day].join('-');
}
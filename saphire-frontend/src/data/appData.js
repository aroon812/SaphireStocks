
export const getStockData = (company) => {
    return massageData(searchStock(company));

}

export const getStockNews = (company) => {
    return searchNews(company);
}


function searchStock(ticker) {
    var theUrl = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker + '&outputsize=full&apikey=23V86RX6LO5AUIX4';
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );

    var json = JSON.parse(xmlHttp.responseText);

    return json['Time Series (Daily)'];
}

function massageData(obj) {
    var result = "[";

    for (var day in obj) {
        result += "{ \"Date\": \"\/Date(" + new Date(day).getTime() + ")\/\""
                + ",\"Close\": " + obj[day]["4. close"] 
                + ", \"Volume\": " + obj[day]["5. volume"] 
                + ", \"Open\": " + obj[day]["1. open"] 
                + ", \"High\": " + obj[day]["2. high"] 
                + ", \"Low\": " + obj[day]["3. low"] + "},";
    }

    result = result.substring(0, result.length - 1);
    result += "]";

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

    return json.articles;;
}
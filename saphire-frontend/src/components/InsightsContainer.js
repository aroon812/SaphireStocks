import React from 'react';
import { Grid, GridColumn as Column } from '@progress/kendo-react-grid';

function searchStock(ticker) {
    var theUrl = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker + '&outputsize=full&apikey=YVHHU0MSRH0ZO8ZQ';
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );

    var json = JSON.parse(xmlHttp.responseText);

    return json;
}

export const InsightsContainer = () => (
    <div>
        <p>{searchStock('MSFT')}</p>
    </div>
);
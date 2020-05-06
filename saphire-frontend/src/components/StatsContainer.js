import React from 'react';

import {Grid, GridColumn as Column } from '@progress/kendo-react-grid';
import {getStockData} from '../data/appData';

function getMostRecent(ticker) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", "http://129.114.16.219:8000/api/stocks/recentInfo/", false);
    xmlHttp.setRequestHeader("Content-Type","application/json");
    xmlHttp.send(JSON.stringify({ ticker: ticker}));
    var json = JSON.parse(xmlHttp.responseText);
    return json;
}

export class StatsContainer extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            ticker: props.ticker,
            name: props.name,
            now: new Date(Date.now()),
        }
    }
    render() {
        return (
            <div className="col-12"> 
            <div className="row"> 
                <div className="col">
                </div>
            </div>
            <div className="row">
                <p>{getMostRecent(this.state.ticker)}</p> 
            </div>
        </div>
        );
    }
}
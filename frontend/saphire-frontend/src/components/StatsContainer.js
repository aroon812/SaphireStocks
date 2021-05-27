import React from 'react';


function getData(ticker) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", "http://127.0.0.1:8000/api/stocks/recentInfo/", false);
    xmlHttp.setRequestHeader("Content-Type","application/json");
    xmlHttp.send(JSON.stringify({ ticker: ticker}));
    var json = JSON.parse(xmlHttp.responseText);
    console.log(json);
    return json;
}

function getSign(oldVal, newVal){ //aaron*
    if (oldVal - newVal > 0){
        return "-";
    } else {
        return "+"
    }
}


export class StatsContainer extends React.Component{
    constructor(props){
        super(props);
        const data = getData(props.ticker);
        this.state = {
            ticker: props.ticker,
            name: props.name,
            now: new Date(Date.now()),
            data: data,
        }
    }

    componentWillReceiveProps(nextProps) {
        const data = getData(nextProps.ticker)
        this.setState({ data: data,
                        ticker: nextProps.ticker,
                        now: new Date(Date.now()),
                        name: nextProps.name, });  
    }  


    render() { 
        return (
            <div className="d-flex">

                <div className="row">
                    <div className="d-flex">

                        <div className="col">

                            <div className="row-md">

                                <h3>Current Price:&nbsp;</h3> <h3  className="black">${this.state.data["current_price"].toFixed(2)}</h3>   

                            </div>

                            <div className="row-md">

                                <h3>Volume:&nbsp;</h3> <h3 className="black"  >{this.state.data["vol"].toFixed()}</h3>   

                            </div>

                        </div>
                    </div>
                    <div className="d-flex">
                        <div className="col-md">

                            <div className="row-md">

                                <h3>Open:&nbsp;</h3> <h3 className="black" >${this.state.data["open"].toFixed(2)}</h3>

                            </div>

                            <div className="row-md">

                                <h3>52 Day High:&nbsp;</h3> <h3 className="black"  >${this.state.data["52_day_high"].toFixed(2)}</h3>

                            </div>

                        </div>
                    </div>
                    <div className="d-flex">
                        <div className="col-md">

                            <div className="row-md">

                                <h3>Percent Change:&nbsp;</h3> <h3 className="black" >{getSign(this.state.data["current-price"],this.state.data["previous_close"])}{this.state.data["percent_change"].toFixed(2)}%</h3>
                            
                            </div>

                            <div className="row-md">

                                <h3>52 Day Low:&nbsp;</h3> <h3 className="black"  >${this.state.data["52_day_low"].toFixed(2)}</h3>   

                            </div>

                        </div>
                    </div>
                    <div className="d-flex">
                        <div className="col-md">

                            <div className="row-md">

                                <h3>Previous Close:&nbsp;</h3> <h3 className="black" >${this.state.data["previous_close"].toFixed(2)}</h3>

                            </div>
                            
                            <div className="row-md">

                                <h3>12 Day EMA:&nbsp;</h3> <h3 className="black"  >${this.state.data["12_day_ema"].toFixed(2)}</h3>

                            </div>

                        </div>
                    </div>
                    <div className="d-flex">
                        <div className="col-md">

                            <div className="row-md">

                                <h3>Range:&nbsp;</h3> <h3 className="black"  >${this.state.data["range"].toFixed(2)}</h3>

                            </div>

                            <div className="row-md">

                                <h3>26 Day EMA:&nbsp;</h3> <h3 className="black"  >${this.state.data["26_day_ema"].toFixed(2)}</h3>  

                            </div>

                        </div>
                    </div>
                    <div className="d-flex">
                        <div className="col-md">

                            <div className="row-md">
                                
                                <h3>Stochastic Oscillator:&nbsp;</h3> <h3 className="black"  >{this.state.data["stochastic_oscillator"].toFixed(2)}%</h3>

                            </div>

                            <div className="row-md">

                                <h3>20 Day Standard Deviation:&nbsp;</h3> <h3 className="black"  >${this.state.data["20_day_stdev"].toFixed(2)}</h3>  

                            </div>
                            
                        </div>
                    </div>
                </div>

            </div>
        );
    }
}
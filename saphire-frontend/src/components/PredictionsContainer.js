import React from 'react';
import {
    Chart,
    ChartTooltip,
    ChartSeries,
    ChartSeriesItem,
    ChartCategoryAxis,
    ChartCategoryAxisItem,
    ChartValueAxis,
    ChartValueAxisItem
  } from '@progress/kendo-react-charts';
import {formatDate} from '../data/appData';

const tempPlotBands = [{
    from: 80, to: 100, color: 'blue', opacity: 1
},{
    from: 60, to: 80, color: 'green', opacity: 1
},{
    from: 40, to: 60, color: 'yellow', opacity: 1
}, {
    from: 20, to: 40, color: 'orange', opacity: 1
}, {
    from: 0, to: 20, color: 'red', opacity: 1
}];


const tooltipRender = ({ point }) => {
    const { value } = point;

    return (
      <span>
        Confidence Level: {value.current}     
      </span>
    )
};

function getData(ticker, date){
    var xmlHttp = new XMLHttpRequest();
    
    xmlHttp.open("POST", "http://127.0.0.1:8000/api/predict/", false);
    xmlHttp.setRequestHeader("Content-Type","application/json");
    xmlHttp.send( JSON.stringify({ticker: ticker, date: date}));
    

    if (xmlHttp.status === 200){
        var json = JSON.parse(xmlHttp.responseText);
        return json;
    }
    else{
        return null;
    }
}

function getSign(oldVal, newVal){ //aaron*
    if (oldVal - newVal > 0){
        return "-";
    } else {
        return "+"
    }
}

function getWords(sign){
    if (sign === "+"){
        return "Positive";
    }
    return "Negative";
}

export class PredictionContainer extends React.Component {
    constructor(props){
        super(props);
        const now = new Date(Date.now());
        const val = getData(props.ticker, formatDate(now));
        this.state = {
            hidden: { visible: false },
            ticker: props.ticker,
            date: now,
            data: val,
        }
    }
    
    componentWillReceiveProps(nextProps) {
        const now = new Date(Date.now());
        const val = getData(nextProps.ticker, formatDate(now));
        this.setState({ 
            hidden: { visible: false },
            ticker: nextProps.ticker,
            date: now,
            data: val,
        });
    }  


    render() {
        return (
            <div className="d-flex">
                <div className="row">
                    <div className="d-flex">
                        <div className="col">
                            <div className="row-md" >
            
                                <h3>Current Price:&nbsp;</h3> <h3 className="black" >${this.state.data["current_price"].toFixed(2)}</h3>

                            </div>

                            <div className="row-md">

                                <h3>Previous Close:</h3> <h3 className="black"  >${this.state.data["last_day_close"].toFixed(2)}</h3>         

                            </div>
                        </div>    
                    </div>
                        <div className="col">
                            <div className="row-md" >
            
                                <h3>Predicted Movement:&nbsp;</h3> <h3 className="black"  >{getWords(this.state.data["directional_prediction"])}</h3>

                            </div>

                            <div className="row-md">

                                <h3>Predicted Next Day Close:</h3> <h3 className="black"  >${this.state.data["projected_price"].toFixed(2)}</h3>         

                            </div>
                        </div>    
                    </div>
                    <div className="d-flex">
                        <div className="col">
                            <div className="row-md">

                                <h3>+3% Five Day Boom:</h3> <h3 className="black"  >{this.state.data["five_day_boom"]}</h3> 

                            </div>
                            <div className="row-md" >
            
                                <h3>Predicted Percent Change:&nbsp;</h3> <h3 className="black" >{getSign(this.state.data["last_day_close"], this.state.data["projected_price"])}{this.state.data["percentage_change"].toFixed(3)}%</h3>

                            </div>
                        </div>    
                    </div> 
                    <div className="d-flex">
                        <div className="col">
                            <div className="row">
                                <h3>+3% Five Day Boom Confidence:</h3>
                            </div>
                            <div className="row">
                                <Chart style={{ height: 50 }} > 
                                        <ChartSeries>
                                            <ChartSeriesItem type="bullet" color="#fff" data={[this.state.data["five_day_boom_confidence"].toFixed()]} />
                                        </ChartSeries>
                                    <ChartCategoryAxis>
                                        <ChartCategoryAxisItem majorGridLines={this.state.hidden} minorGridLines={this.state.hidden} />
                                    </ChartCategoryAxis>
                                    <ChartValueAxis>
                                        <ChartValueAxisItem majorGridLines={this.state.hidden} minorTicks={this.state.hidden} min={0} max={99} plotBands={tempPlotBands} />
                                    </ChartValueAxis>
                                    <ChartTooltip render={tooltipRender} />
                                </Chart> 
                        </div>
                    </div>     
                </div>
            </div>
            
        );
    }
}


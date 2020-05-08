import React from 'react';
import {
    Chart,
    ChartTitle,
    ChartTooltip,
    ChartSeries,
    ChartSeriesItem,
    ChartCategoryAxis,
    ChartCategoryAxisItem,
    ChartValueAxis,
    ChartValueAxisItem
  } from '@progress/kendo-react-charts';
import {Grid, GridColumn as Column } from '@progress/kendo-react-grid';
import {getStockNews} from '../data/appData';

const tempPlotBands = [{
    from: 30, to: 45, color: '#e62325', opacity: 1
}, {
    from: 15, to: 30, color: '#ffc000', opacity: 1
}, {
    from: 0, to: 15, color: '#37b400', opacity: 1
}, {
    from: -10, to: 0, color: '#5392ff', opacity: 1
}];
const humPlotBands = [{
    from: 0, to: 33, color: '#ccc', opacity: .6
}, {
    from: 33, to: 66, color: '#ccc', opacity: .3
}];
const mmhgPlotBands = [{
    from: 715, to: 752, color: '#ccc', opacity: .6
}, {
    from: 752, to: 772, color: '#ccc', opacity: .3
}];

const temp = [[25, 22]];

const tooltipRender = ({ point }) => {
    const { value } = point;

    return (
      <span>
        Maximum: { value.target }
        <br />
        Average: { value.current }
      </span>
    )
  };


export class PredictionContainer extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            hidden: { visible: false },
            symbol: 'A',
        }
    }

    render() {
        return (
            <div className="container">
    
                <div className="row">


                    <div className="col-4">
    
                        <div className="row-md" >
    
                            <h3>Percent Change:&nbsp;</h3> <h3 className="black" >{}%</h3>
    
                        </div>

                        <div className="row-md">
    
                            <h3>volatility (%):&nbsp;</h3> <h3 className="black"  >${}</h3>

                        </div>
    
                    </div>

    
                    <div className="col-4">
                        <div className="row-md">
                            <Chart style={{ height: 120 }} >
                                <ChartTitle text="Temperature [&deg;C]" />
                                    <ChartSeries>
                                        <ChartSeriesItem type="bullet" color="#fff" data={temp} />
                                    </ChartSeries>
                                <ChartCategoryAxis>
                                    <ChartCategoryAxisItem majorGridLines={this.state.hidden} minorGridLines={this.state.hidden} />
                                </ChartCategoryAxis>
                                <ChartValueAxis>
                                    <ChartValueAxisItem majorGridLines={this.state.hidden} minorTicks={this.state.hidden} min={-10} max={45} plotBands={tempPlotBands} />
                                </ChartValueAxis>
                                <ChartTooltip render={tooltipRender} />
                            </Chart>                        
                        
    
                            <h3>Confidence (High/Low):&nbsp;</h3> <h3 className="black" >${}</h3>
    
                        </div>
    
                    </div>
    
    
                    <div className="col-4">

                        <div className="row-md">
    
                            <h3>Predicted Price ($):</h3> <h3 className="black"  >{}</h3>  
    
                        </div>
    
    
                        <div className="row-md">
    
                            <h3>Predicted Movement (+/-):</h3> <h3 className="black"  >${}</h3>  
    
                        </div>
    
                    </div>
    
                </div>
    
            </div>
        );
    }
}


import React from "react";
import {
  StockChart,
  ChartTitle,
  ChartSeries,
  ChartSeriesItem,
  ChartNavigator,
  ChartNavigatorSelect,
  ChartNavigatorSeries,
  ChartNavigatorSeriesItem
} from "@progress/kendo-react-charts";
import { IntlService } from '@progress/kendo-react-intl';
import { filterBy } from '@progress/kendo-data-query';
import { Button, ButtonGroup, Toolbar, ToolbarItem } from '@progress/kendo-react-buttons';
import "hammerjs";
import {getStockData} from '../data/appData';


var toU = new Date(Date.now()); 
var fromU = new Date(Date.now());
fromU = new Date(fromU.setFullYear( fromU.getFullYear() - 5 ));
const to = toU.toDateString();
const from = fromU.toDateString();

const intl = new IntlService('en');

function mapper(data) {
  return data.map(item => (Object.assign({}, item, { Date: intl.parseDate(item.Date)})));
}

function getName(symbol) {
  var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", 'http://127.0.0.1:8000/api/companies/' + symbol + '/', false); // false for synchronous request
    xmlHttp.setRequestHeader("Content-Type","application/json");
    xmlHttp.send(JSON.stringify({ symbol: symbol }));
   
    if (xmlHttp.status===200){
      console.log(xmlHttp.responseText);
      var json = JSON.parse(xmlHttp.responseText);
      console.log(json);
      return json['name'];
    }
    return null;
}

export class StockChartContainer extends React.Component {
  constructor(props){
    super(props);
    const data = getStockData(props.symbol, fromU, to);
    const stockData = mapper(data);
    this.state = {
      ticker: props.symbol,
      name: getName(props.symbol),
      seriesData: Array.from(stockData),
      navigatorData: Array.from(stockData),
      selected: 0,
    }
  }

 

  render() {
    const { seriesData, navigatorData } = this.state;
    console.log(seriesData);
    console.log(navigatorData)
    return (
        <StockChart onNavigatorFilter={this.onNavigatorChange} partialRedraw={true}>
            <ChartTitle text= {this.state.name + "[" + this.state.ticker + "]"} />
            <ChartSeries>
                <ChartSeriesItem
                    data={seriesData}
                    type="candlestick"
                    openField="Open"
                    closeField="Close"
                    lowField="Low"
                    highField="High"
                    categoryField="Date"
                />
            </ChartSeries>
            <ChartNavigator>
                <ChartNavigatorSelect from={from} to={to} />
                <ChartNavigatorSeries>
                    <ChartNavigatorSeriesItem
                        data={navigatorData}
                        type="area"
                        field="Close"
                        categoryField="Date"
                    />
                </ChartNavigatorSeries>
            </ChartNavigator>
        </StockChart>
    );
  }

  onNavigatorChange = (event) => {
    const filters = {
        logic: 'and',
        filters: [{
            field: 'Date',
            operator: 'gte',
            value: event.from
        }, {
            field: 'Date',
            operator: 'lt',
            value: event.to
        }]
    };

    this.setState((prevState) => ({
        seriesData: filterBy(prevState.navigatorData, filters)
    }));
  }
}
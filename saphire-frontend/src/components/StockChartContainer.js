import React from "react";
import {
  StockChart,
  ChartSeries,
  ChartSeriesItem,
  ChartNavigator,
  ChartNavigatorSelect,
  ChartNavigatorSeries,
  ChartNavigatorSeriesItem
} from "@progress/kendo-react-charts";
import { IntlService } from '@progress/kendo-react-intl';
import { filterBy } from '@progress/kendo-data-query';
import "hammerjs";
import {getStockData} from '../data/appData';


var toU = new Date(Date.now()); 
var fromU = new Date(Date.now());
fromU = new Date(fromU.setFullYear( fromU.getFullYear() - 5 ));

const intl = new IntlService('en');

function mapper(data) {
  return data.map(item => (Object.assign({}, item, { Date: intl.parseDate(item.Date)})));
}




export class StockChartContainer extends React.Component {
  constructor(props){
    super(props);
    const data = getStockData(props.ticker, fromU, toU);
    const stockData = mapper(data);
    this.state = {
      ticker: props.ticker,
      name: props.name,
      seriesData: Array.from(stockData),
      navigatorData: Array.from(stockData),
      selected: 0,
      to: toU,
      from: fromU,
    }
  }

  componentWillReceiveProps(nextProps) {
    const data = getStockData(nextProps.ticker, fromU, toU);
    const stockData = mapper(data);
    this.setState({ 
                    ticker: nextProps.ticker,
                    name: nextProps.name,
                    seriesData: Array.from(stockData),
                    navigatorData: Array.from(stockData),
                    to: toU,
                    from: fromU,
                  });  
  }  



  
  render() {
    const { seriesData, navigatorData, ticker, name } = this.state;
    return (
        <div>
          <div>
            <div className="stockName">
              <h4>{name} [{ticker}]</h4> 
            </div>
            <StockChart onNavigatorFilter={this.onNavigatorChange} partialRedraw={true}>
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
                    <ChartNavigatorSelect from={this.state.from} to={this.state.to} />
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
          </div>
        </div>
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
import React from 'react';
import { Grid, GridColumn as Column } from '@progress/kendo-react-grid';
import { Sparkline } from '@progress/kendo-react-charts';
import { Button } from '@progress/kendo-react-buttons';
import {getWatchedStocksData} from '../data/appData';

const SparkLineChartCell = (props) => <td><Sparkline data={props.dataItem.PriceHistory}/></td>

export class MyStocksContainer extends React.Component {
  constructor(props) {
    super(props);
    
    this.state = {
      name: props.name,
      ticker: props.ticker,
      data: getWatchedStocksData()
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ 
      name: nextProps.name,
      ticker: nextProps.ticker,
      data: getWatchedStocksData()
      });
    }  


     removeStock = (ticker) => {
      var token = localStorage.getItem("token");
      var xmlHttp = new XMLHttpRequest();
    
      xmlHttp.open("DELETE", "http://127.0.0.1:8000/api/watchStock/", false);
      xmlHttp.setRequestHeader("Content-Type","application/json");
      xmlHttp.setRequestHeader("Authorization", "Token " + token);
      xmlHttp.send(JSON.stringify({ symbol: ticker }));
      this.componentWillReceiveProps(this.state);
    }
    
    addStock = (ticker) => {
      var token = localStorage.getItem("token");
      console.log(ticker);
      var xmlHttp = new XMLHttpRequest();
      xmlHttp.open("POST", "http://127.0.0.1:8000/api/watchStock/", false);
      xmlHttp.setRequestHeader("Content-Type","application/json");
      xmlHttp.setRequestHeader("Authorization", "Token " + token);
      xmlHttp.send(JSON.stringify({ symbol: ticker }));

      this.componentWillReceiveProps(this.state);
    }

    changeStock = (ticker) => {
      this.props.handleTickerChange(ticker);
      this.componentWillReceiveProps(this.state);
    }

    containsTicker = () => {
      for (var obj in this.state.data){
        console.log(this.state.data[obj]['Ticker']);
        if (this.state.data[obj]['Ticker'] === this.state.ticker){
          return true;
        }
      }
      return false;
    }


    
  render () {
  return (
    <div>
      <div>{ 
        (!this.containsTicker() && <Button primary={true} onClick={() => this.addStock(this.state.ticker)}>Add {this.state.name} to My Stocks</Button>)
        ||
        (this.containsTicker()  && <Button primary={true} onClick={() => this.removeStock(this.state.ticker)}>Remove {this.state.name} from My Stocks</Button>)
      }
      </div> 
      <div>
        <Grid style={{ height: '325px' }} data={this.state.data}>
          <Column field="Ticker" title="Ticker" width="100px" cell={(props) => (
              <td>
                <Button primary={true} onClick={() => this.changeStock(props['dataItem']['Ticker'])}>{props['dataItem']['Ticker']}</Button>
              </td>
            )} />
          <Column field="PriceHistory" width="150px" cell={SparkLineChartCell} title="Price history" />
          <Column field="Action" width="100px"
            cell={(props) => (
              <td>
                <Button primary={true} onClick={() => this.removeStock(props['dataItem']['Ticker'])}>-</Button>
              </td>
            )} />
        </Grid>
      </div>
    </div>
  );
            }
}
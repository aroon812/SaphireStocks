import React from 'react';
import { Grid, GridColumn as Column } from '@progress/kendo-react-grid';
import { Sparkline } from '@progress/kendo-react-charts';
import { Button } from '@progress/kendo-react-buttons';
import {getWatchedStocksData} from '../data/appData';

const SparkLineChartCell = (props) => <td><Sparkline data={props.dataItem.PriceHistory}/></td>

const removeStock = (ticker) => {
  var token = localStorage.getItem("token");
  var xmlHttp = new XMLHttpRequest();

  xmlHttp.open("DELETE", "http://129.114.16.219:8000/api/watchStock/", false);
  xmlHttp.setRequestHeader("Content-Type","application/json");
  xmlHttp.setRequestHeader("Authorization", "Token " + token);
  xmlHttp.send(JSON.stringify({ symbol: ticker }));
}

const addStock = (ticker) => {
  var token = localStorage.getItem("token");
  console.log(ticker);
  var xmlHttp = new XMLHttpRequest();

  xmlHttp.open("POST", "http://129.114.16.219:8000/api/watchStock/", false);
  xmlHttp.setRequestHeader("Content-Type","application/json");
  xmlHttp.setRequestHeader("Authorization", "Token " + token);
  xmlHttp.send(JSON.stringify({ symbol: ticker }));
}

export const MyStocksContainer = (props) => {
  const data = getWatchedStocksData();

  return (
    <div>
      <div>
        <Button primary={true} onClick={() => addStock(props.ticker)}>Add {props.name} to My Stocks</Button>
      </div> 
      <div>
        <Grid style={{ height: '325px' }} data={data}>
          <Column field="Ticker" title="Ticker" width="100px" />
          <Column field="PriceHistory" width="150px" cell={SparkLineChartCell} title="Price history" />
          <Column field="Action" width="100px"
            cell={(props) => (
              <td>
                <Button primary={true} onClick={() => removeStock(props['dataItem']['Ticker'])}>-</Button>
              </td>
            )} />
        </Grid>
      </div>
    </div>
  );
}

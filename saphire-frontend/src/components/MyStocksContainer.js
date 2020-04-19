import React from 'react';
import { Grid, GridColumn as Column } from '@progress/kendo-react-grid';
import { Sparkline } from '@progress/kendo-react-charts';
import { Button } from '@progress/kendo-react-buttons';
import {getWatchedStocksData} from '../data/appData';

const SparkLineChartCell = (props) => <td><Sparkline data={props.dataItem.PriceHistory}/></td>
const processData = (data) => {
  data.forEach((item) => {
    console.log(item);
  })
  return data;
}

export const MyStocksContainer = () => {
  const data = getWatchedStocksData();


  return (
    <div>
      
      <Grid style={{ height: '435px' }} data={data}>
        <Column field="Ticker" title="Ticker" width="100px" />
        <Column field="PriceHistory" width="150px" cell={SparkLineChartCell} title="Price history" />
        <Column field="Action" width="100px"
          cell={(props) => (
            <td>
              <Button primary={true}>-</Button>
            </td>
          )} />
      </Grid>
    </div>
  );
}

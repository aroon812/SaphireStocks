import React from 'react';
import { Grid, GridColumn as Column } from '@progress/kendo-react-grid';
import { Sparkline } from '@progress/kendo-react-charts';
import { Button } from '@progress/kendo-react-buttons';

const SparkLineChartCell = (props) => <td><Sparkline data={props.dataItem.PriceHistory}/></td>
const processData = (data) => {
  data.forEach((item) => {
    item.PriceHistory = Array.from({ length: 20 }, () => Math.floor(Math.random() * 100));
    return item;
  })
  return data;
}

export const MyStocksContainer = () => (

  <div>
    <Grid style={{ height: '435px' }} data="">
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
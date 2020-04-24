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
import "hammerjs";

import {getStockData} from '../data/appData';


export const StockChartContainer = (prop) => {
  const data = getStockData(prop.symbol);

  const from = new Date("2000-03-06");
  const to = new Date(Date.now());

  

  return (
    <StockChart>
        <ChartTitle text={`${prop.company} - ${prop.symbol}`} />
        <ChartSeries>
            <ChartSeriesItem
                data={data}
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
                    data={data}
                    type="area"
                    field="Close"
                    categoryField="Date"
                />
            </ChartNavigatorSeries>
        </ChartNavigator>
    </StockChart>
  );
}
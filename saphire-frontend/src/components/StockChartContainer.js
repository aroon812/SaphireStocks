
import React from 'react';
import 'hammerjs';

import {
    StockChart,
    ChartTitle,
    ChartSeries,
    ChartSeriesItem,
    ChartNavigator,
    ChartNavigatorSelect,
    ChartNavigatorSeries,
    ChartNavigatorSeriesItem
} from '@progress/kendo-react-charts';

import stockData from '../data/stock-data.json';

const from = new Date('2009/02/05');
const to = new Date('2011/10/07');

export const StockChartContainer = () => (
    <StockChart>
        <ChartTitle text="The Boeing Company NYSE:BA" />
        <ChartSeries>
            <ChartSeriesItem
                data={stockData}
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
                    data={stockData}
                    type="area"
                    field="Close"
                    categoryField="Date"
                />
            </ChartNavigatorSeries>
        </ChartNavigator>
    </StockChart>
);

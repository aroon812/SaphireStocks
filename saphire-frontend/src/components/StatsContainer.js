import React from 'react';

import {Grid, GridColumn as Column } from '@progress/kendo-react-grid';
import {getStockNews} from '../data/appData';


export const StatsContainer = (prop) => (
    <div className="col-12"> 
        <div className="row"> 
        
        </div>
        <div className="row">
            <Grid style={{ height: '300' }} data={getStockNews(prop.symbol)}>
                <Column title="Percent Change (%)" field="urlToImage" width="150" cell="SampleText"/>
                <Column title="Confidence (%)" field="urlToImage" width="200" cell="SampleText" />
                <Column title="volatility (High/Low)" field="urlToImage" width="200" cell="SampleText" />
                <Column title="Predicted Movement (+/-)" field="urlToImage" width="250" cell="SampleText" />
                <Column title="Predicted Price ($)" field="urlToImage" width="175" cell="SampleText" />
            </Grid>
        </div>
    </div>
);
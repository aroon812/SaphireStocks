import React from 'react';

import {Grid, GridColumn as Column } from '@progress/kendo-react-grid';
import {getStockNews} from '../data/appData';


export class PredictionContainer extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            symbol: 'A',
        }
    }

    render(){
        return (
            <div className="col-12"> 
                <div className="row"> 
                
                </div>
                <div className="row">
                    <Grid style={{ height: '300' }} data={getStockNews(this.symbol)}>
                        <Column title="Percent Change (%)" field="urlToImage" width="150" cell="SampleText"/>
                        <Column title="Confidence (High/Low)" field="urlToImage" width="200" cell="SampleText" />
                        <Column title="volatility (%)" field="urlToImage" width="200" cell="SampleText" />
                        <Column title="Predicted Movement (+/-)" field="urlToImage" width="250" cell="SampleText" />
                        <Column title="Predicted Price ($)" field="urlToImage" width="175" cell="SampleText" />
                    </Grid>
                </div>
            </div>
        );
    }
}
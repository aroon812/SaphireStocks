import React from 'react';

import {Grid, GridColumn as Column } from '@progress/kendo-react-grid';
import {getStockNews} from '../data/appData';

const artImg = (props) => <img className="newsImg" width="150" height="100" alt="News IMG" src={props.dataItem.urlToImage}/>

export const NewsContainer = (props) => (
    <div>
        <Grid style={{ height: '400px' }} data={getStockNews(props.name)}>
            <Column title={props.name + " [" + props.ticker + "]"} field="urlToImage" width="250px" cell={artImg} />
            <Column title=" " field="title" cell={(props) => (
                <td>
                    <a href={props.dataItem.url} rel="noopener noreferrer" target="_blank">
                        <h4>{props.dataItem.title}</h4>
                    </a>
                </td>
                )} />
        </Grid>
    </div>
);
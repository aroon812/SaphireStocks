import React from 'react';

import {Grid, GridColumn as Column } from '@progress/kendo-react-grid';
import {getStockNews} from '../data/appData';

const Header = (text) => (
    <span>
        <h3>{text}</h3>
    </span>
    
)


const artImg = (props) => <img className="newsImg" width="150" height="100" alt="No Image" src={props.dataItem.urlToImage}/>


export const NewsContainer = (prop) => (
    <div>
        <Grid style={{ height: '400px' }} data={getStockNews(prop.symbol)}>
            <Column title="Articles" field="urlToImage" width="200px" cell={artImg} />
            <Column title=" " field="title" cell={(props) => (
                <td>
                    <a href={props.dataItem.url} target="_blank">
                        <h4>{props.dataItem.title}</h4>
                    </a>
                </td>
                )} />
        </Grid>
    </div>
);
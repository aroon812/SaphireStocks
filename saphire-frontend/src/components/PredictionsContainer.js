import React from 'react';
import { Grid, GridColumn as Column } from '@progress/kendo-react-grid';

const Header = (text) => (
    <span>
        <h3>{text}</h3>
    </span>
    
)

export const PredictionContainer = () => (
    <div>
        <Grid style={{ height: '312px' }}>
            <Column field="Day" title={Header("Day")} width="100px" />
            <Column field="Prediction" title={Header("Prediction")} width="125px" />
            <Column field="Confidence" title={Header("Confidence")} width="125px"
                cell={(props) => (
                    <td>
                    </td>
            )} />
        </Grid>
    </div>
);
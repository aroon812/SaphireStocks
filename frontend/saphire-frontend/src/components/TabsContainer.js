import React from "react";
import { TabStrip } from '@progress/kendo-react-layout';
import { TabStripTab } from '@progress/kendo-react-layout';
import { PredictionContainer } from './PredictionsContainer';
import { NewsContainer } from './NewsContainer';
import { StatsContainer } from './StatsContainer';


export class TabsContainer extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            selected: 0,
            ticker: props.ticker,
            name: props.name,
        }
    }

    componentWillReceiveProps(nextProps) {
        this.setState({ selected: this.state.selected,
                        ticker: nextProps.ticker,
                        name: nextProps.name, });  
    }   

    handleSelect = (e) => {
        this.setState({selected: e.selected})
    }

    Header4 = (text) => (
        <h4>{text}</h4>
    )

    render(){
        return (
            <TabStrip  selected={this.state.selected} onSelect={this.handleSelect} >
                <TabStripTab title={this.Header4("AI Insights")}>
                    <PredictionContainer ticker={this.state.ticker} name={this.state.name}/>
                </TabStripTab>
                <TabStripTab title={this.Header4("Statistics")}>
                    <StatsContainer ticker={this.state.ticker} name={this.state.name}/>
                </TabStripTab>   
                <TabStripTab title={this.Header4("News")}>
                    <NewsContainer ticker={this.state.ticker} name={this.state.name}/>
                </TabStripTab>
            </TabStrip>
        );
    }
}



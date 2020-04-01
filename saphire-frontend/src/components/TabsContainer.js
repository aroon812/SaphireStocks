import { TabStrip } from '@progress/kendo-react-layout';
import { TabStripTab } from '@progress/kendo-react-layout';
import { PredictionContainer } from './components/PredictionsContainer';
import { NewsContainer } from './components/NewsContainer';
import { InsightsContainer } from './components/InsightsContainer';



export const TabsContainer = (props) => {
    return (
        <TabStrip  selected={this.state.selected} onSelect={this.handleSelect} >
            <TabStripTab title={this.Header4("Statistics")}>

            </TabStripTab>
            <TabStripTab title={this.Header4("Insights")}>
                <InsightsContainer />
            </TabStripTab>   
            <TabStripTab title={this.Header4("News")}>
                <NewsContainer symbol={props.symbol} />
            </TabStripTab>
        </TabStrip>
    );
}



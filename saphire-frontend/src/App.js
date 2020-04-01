

import { Dialog, DialogActionsBar } from '@progress/kendo-react-dialogs';
import { Input } from '@progress/kendo-react-inputs'; 
import { Button, ButtonGroup, Toolbar, ToolbarItem } from '@progress/kendo-react-buttons';
import { Ripple } from '@progress/kendo-react-ripple';
import { savePDF } from '@progress/kendo-react-pdf';
import { TabStrip } from '@progress/kendo-react-layout';
import { TabStripTab } from '@progress/kendo-react-layout';

import Logo from './img/saphireLogo.png';


import { StockChartContainer } from './components/StockChartContainer';
import { MyStocksContainer } from './components/MyStocksContainer';

import { PredictionContainer } from './components/PredictionsContainer';
import { NewsContainer } from './components/NewsContainer';
import { InsightsContainer } from './components/InsightsContainer';


import React, { Component } from 'react';
import ReactDOM from 'react-dom';

import '@progress/kendo-theme-material/dist/all.css';
import './App.css';
import 'bootstrap-4-grid/css/grid.min.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.appContainer = React.createRef();
    this.state = {
      showDialog: false,
      selected: 0
    }
  }
  
  handlePDFExport = () => {
    savePDF(ReactDOM.findDOMNode(this.appContainer), { paperSize: 'auto' });
  }

  handleShare = () => {
    this.setState({
      showDialog: !this.state.showDialog
    }, () => console.log(this.state))
  }

  handleLogin = () => {
    this.setState({ 
      showLogin: !this.state.showLogin
    }, () => console.log(this.state))
  }

  handleRegistration = () => {
    this.setState({
      showResgistration: !this.state.showResgistration
    }, () => console.log(this.state))
  }

  
  handleSelect = (e) => {
      this.setState({selected: e.selected})
  }

  Header4 = (text) => (
    <h4>{text}</h4>
  )

  

  render() {
    return (
      <Ripple>
        <div className="bootstrap-wrapper">
          <div className="app-container container" ref={(el) => this.appContainer = el}> 
            <div className="row">
							<div className="col-sm-6">
                <div className="row-xs">
                  <img src={Logo} alt="Logo" width="325" height="85" />
                </div>
						  </div>
							<div className="col-sm-6 buttons-right">
                  <Toolbar className="float-right d-flex">
                    <ToolbarItem className="float-right d-flex">
                      <div className="littleSearchBar">
                        <Input label="Search..." />
                      </div>
                      <Button className="float-right" onClick={this.handlePDFExport}>Export as PDF</Button>               
                      <Button className="float-right" onClick={this.handleShare}>Share</Button> 
                      <Button className="float-right" onClick={this.handleLogin}>Sign In</Button>
                    </ToolbarItem>
                  </Toolbar>
							</div>
					  </div>
            <div className="row">
              <div className="col-8">
								<StockChartContainer symbol='AAPL' company={'Apple'} />
						  </div>
              <div className="col-4">
                <h3>AI Predictions</h3>
                <PredictionContainer />
							</div>
            </div>
            <div className="row">
              <div className="col-8">
                <div>
                  <TabStrip  selected={this.state.selected} onSelect={this.handleSelect} >
                    <TabStripTab title={this.Header4("Statistics")}>
                      
                    </TabStripTab>

                    <TabStripTab title={this.Header4("Insights")}>
                      <InsightsContainer />
                    </TabStripTab>   
                    <TabStripTab title={this.Header4("News")}>
                      <NewsContainer symbol='AAPL' />
                    </TabStripTab>
                  </TabStrip>
                </div>
              </div>
              <div className="col-4">
                <h3>My Stocks</h3>
								<MyStocksContainer />
              </div>
            </div>
            {this.state.showDialog &&
							<Dialog title={"Share this report"} onClose={this.handleShare}>
								<p>Please enter the email address/es of the recipient/s.</p>
								<Input placeholder="example@Email.com" />
								<DialogActionsBar>
									<Button primary={true} onClick={this.handleShare}>Share</Button>
									<Button onClick={this.handleShare}>Cancel</Button>
								</DialogActionsBar>
							</Dialog>
						}
            {this.state.showLogin &&
							<Dialog title={"Sign In"} onClose={this.handleLogin}>
                <div className="col">
                  <div className="row">
                    <p>Please enter your email and password.</p>
                  </div>
                  <div className="row justify-content-center">
                    <Input label="Email"/>
                  </div>
                  <div className="row justify-content-center">
                    <Input label="Password" />                   
                  </div>
                </div>
              <DialogActionsBar>
                <Button onClick={this.handleRegistration}>Create Account</Button>
                <Button primary={true} onClick={this.handleLogin}>Sign In</Button>
              </DialogActionsBar>
            </Dialog>
						}
            {this.state.showResgistration &&
							<Dialog title={"Create Account"} onClose={this.handleRegistration}>
                <div className="col">
                  <div className="row">
                    <p>Please enter your first name, last name, email and new password.</p>
                  </div>
                  <div className="row justify-content-center">
                    <Input label="First Name" />
                  </div>
                  <div className="row justify-content-center">
                    <Input label="Last Name" />
                  </div>
                  <div className="row justify-content-center">
                    <Input label="Email" />
                  </div>
                  <div className="row justify-content-center">
                    <Input label="Password" />                   
                  </div>
                  <div className="row justify-content-center">
                    <Input label="Confirm Password" />                   
                  </div>
                </div>
              <DialogActionsBar>
                <Button onClick={this.handleRegistration}>Cancel</Button>
                <Button primary={true} onClick={this.handleRegistration}>Create Account</Button>
              </DialogActionsBar>
            </Dialog>
						}
          </div>
        </div>
      </Ripple>
    );
  }
}

export default App;

import React, { Component } from 'react';
import ReactDOM from 'react-dom';
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
import { SignInInput } from './components/SignInInput';
import { RegistrationInput } from './components/RegistrationInput';




import ApexCharts from 'apexcharts'
import '@progress/kendo-theme-material/dist/all.css';
import './App.css';
import 'bootstrap-4-grid/css/grid.min.css'; 
import { TabsContainer } from './components/TabsContainer';

class App extends Component {
  constructor(props) {
    super(props);
    this.appContainer = React.createRef();
    this.handleLoginStateChange = this.handleLoginStateChange.bind(this);
    this.handleRegistrationStateChange = this.handleRegistrationStateChange.bind(this);

    this.state = {
      showDialog: false,
      showLogin: false,
      showResgistration: false,
      selected: 0,
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

  handleLoginStateChange = () => {
    this.setState({showLogin: !this.state.showLogin},
      () => console.log(this.state));
  }

  handleRegistrationStateChange = () => {
    console.log("registration state change test");
    this.setState({
      showResgistration: !this.state.showResgistration
    }, () => console.log(this.state))
    this.handleLoginStateChange();
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
                      <Button className="float-right" onClick={this.handleLoginStateChange}>Sign In</Button>
                    </ToolbarItem>
                  </Toolbar>
							</div>
					  </div>

            <div className="row">
              <div className="col-8">
                <StockChartContainer symbol='AAPL' company={'Apple'} />
						  </div>
              <div className="col-4">
                <h3>My Stocks</h3>
								<MyStocksContainer />
              </div>
            </div>

            <div className="row">
              <div className="col-12">
                <div>
                  <TabsContainer />
                </div>
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
							<SignInInput handleLoginStateChange = {this.handleLoginStateChange} handleRegistrationStateChange = {this.handleRegistrationStateChange}/>
						}
            {this.state.showResgistration &&
              <RegistrationInput handleRegistrationStateChange = {this.handleRegistrationStateChange} />
						}
          </div>
        </div>
      </Ripple>
    );
  }
}

export default App;
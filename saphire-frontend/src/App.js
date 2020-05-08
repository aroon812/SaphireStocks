
import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { Dialog, DialogActionsBar } from '@progress/kendo-react-dialogs';
import { Input } from '@progress/kendo-react-inputs'; 
import { Button, ButtonGroup, Toolbar, ToolbarItem } from '@progress/kendo-react-buttons';
import { Ripple } from '@progress/kendo-react-ripple';
import { savePDF } from '@progress/kendo-react-pdf';

import Logo from './img/saphireLogo.png';


import { StockChartContainer } from './components/StockChartContainer';
import { MyStocksContainer } from './components/MyStocksContainer';
import { SearchInput } from './components/SearchInput'
import { SignInInput } from './components/SignInInput';
import { RegistrationInput } from './components/RegistrationInput';
import { getCompanyData } from './data/appData'

import '@progress/kendo-theme-material/dist/all.css';
import './App.css';
import 'bootstrap-4-grid/css/grid.min.css'; 
import { TabsContainer } from './components/TabsContainer';


function getName(symbol) {
  var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", 'http://129.114.16.219:8000/api/companies/' + symbol + '/', false); // false for synchronous request
    xmlHttp.setRequestHeader("Content-Type","application/json");
    xmlHttp.send(JSON.stringify({ symbol: symbol }));
   
    if (xmlHttp.status===200){
      var json = JSON.parse(xmlHttp.responseText);
      return json['name'];
    }
    return null;
}

class App extends Component {
  constructor(props) {
    super(props);
    this.appContainer = React.createRef();
    this.handleLoginStateChange = this.handleLoginStateChange.bind(this);
    this.handleRegistrationStateChange = this.handleRegistrationStateChange.bind(this);
    var signedIn = false;
    if (localStorage.getItem("token") == "base"){
      signedIn = false;
    }
    else{
      signedIn = true;
    }

    this.state = {
      showDialog: false,
      showLogin: false,
      showResgistration: false,
      selected: 0,
      ticker: "A",
      loggedIn: signedIn
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

  handleQueryChange = event => {
    console.log(event);
    this.setState({ 
      [event.target.name]: event.target.value,
    });
  }

  handleSearch = () => {
    var ticker = getCompanyData(this.state.query);
    this.setState({
      ticker: ticker
    }, () => this.forceUpdate());
  }

  handleSignIn = () => {
    this.handleLoginStateChange();
    this.setState({
      loggedIn: true
    });
  }

  handleSignOut = () => {
    localStorage.setItem("token", "base");
    this.setState({
      loggedIn: false
    });
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
                      <Input label="Search..." name="query" value={this.state.query} onChange={this.handleQueryChange}/>
                      </div>
                      <Button className="float-right" onClick={this.handleSearch}>Search</Button> 
                      <Button className="float-right" onClick={this.handlePDFExport}>Export as PDF</Button>               
                      <Button className="float-right" onClick={this.handleShare}>Share</Button> 
                      {
                        this.state.loggedIn == false &&
                        <Button className="float-right" onClick={this.handleSignIn}>Sign In</Button> 
                        ||
                        this.state.loggedIn == true &&
                        <Button className="float-right" onClick={this.handleSignOut}>Log Out</Button>
                        
                      } 
                    </ToolbarItem>
                  </Toolbar>
							</div>
					  </div>

            <div className="row">
              <div className="col-8">
                <StockChartContainer ticker={this.state.ticker} name={getName(this.state.ticker)}/>
						  </div>
              { this.state.loggedIn == true &&
              <div className="col-4">
                <h3>My Stocks</h3>
								<MyStocksContainer ticker={this.state.ticker} name={getName(this.state.ticker)}/>
              </div> 
              || this.state.loggedIn == false &&
              <div className="col-4">
                <h3>About Saphire</h3>
                <p> saphire is cool </p>
              </div>
              }
            </div>

            <div className="row">
              <div className="col-12">
                <div>
                  <TabsContainer ticker={this.state.ticker} name={getName(this.state.ticker)}/>
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
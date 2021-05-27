
import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { Dialog, DialogActionsBar } from '@progress/kendo-react-dialogs';
import { Input } from '@progress/kendo-react-inputs'; 
import { Button, Toolbar, ToolbarItem } from '@progress/kendo-react-buttons';
import { Ripple } from '@progress/kendo-react-ripple';
import { savePDF } from '@progress/kendo-react-pdf';

import Logo from './img/saphireLogo.png';
import saphireLogo2 from './img/saphireLogo2.png';

import { StockChartContainer } from './components/StockChartContainer';
import { MyStocksContainer } from './components/MyStocksContainer';
import { SearchInput } from './components/SearchInput'
import { SignInInput } from './components/SignInInput';
import { RegistrationInput } from './components/RegistrationInput';

import '@progress/kendo-theme-material/dist/all.css';
import './App.css';
import 'bootstrap-4-grid/css/grid.min.css'; 
import { TabsContainer } from './components/TabsContainer';


function getName(symbol) {
  var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", 'http://127.0.0.1:8000/api/companies/' + symbol + '/', false); // false for synchronous request
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
    if (localStorage.getItem("token") === "base"){
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
      ticker: "AAPL",
      loggedIn: signedIn
    }
  }

  handlePDFExport = () => {
    savePDF(ReactDOM.findDOMNode(this.appContainer), { paperSize: 'auto' });
  }

  searchCallBack = (searchResults) => {
    console.log(searchResults);
    if (searchResults == null){
      alert("Stock does not exist!");
    }
    else{
    this.setState({
      ticker: searchResults
    })
  }
  }

  handleQueryChange = event => {
    console.log(event);
    this.setState({ 
      [event.target.name]: event.target.value,
    });
  }

  handleTickerChange = (ticker) => {
    //var ticker = getCompanyData(this.state.query);
    this.setState({
      ticker: ticker
    });
  }

  handleSignIn = () => {
    this.handleLoginStateChange();
  }

  handleSignOut = () => {
    localStorage.setItem("token", "base");
    this.setState({
      loggedIn: false
    });
  }

  handleSuccessfulSignIn = () => {
    this.setState({
      loggedIn: true,
      showLogin: !this.state.showLogin
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
//<Button className="float-right" onClick={this.handleSearch}>Search</Button> 
/*
<div className="littleSearchBar">
<Input label="Search..." name="query" value={this.state.query} onChange={this.handleQueryChange}/>
</div>
<Button className="float-right" onClick={this.handleSearch}>Search</Button> 
*/

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
                  <img src={Logo} alt="UpperLogo" width="325" height="85" />
                </div>
						  </div>
							<div className="col-sm-6 buttons-right">
                  <Toolbar className="float-right d-flex">
                    <ToolbarItem className="float-right d-flex">
                      <SearchInput callback={this.searchCallBack}/>
                      <Button className="float-right" onClick={this.handlePDFExport}>Export as PDF</Button>               
                      {
                        (this.state.loggedIn === false &&
                        <Button className="float-right" onClick={this.handleLoginStateChange}>Sign In</Button>) 
                        ||
                        (this.state.loggedIn === true &&
                        <Button className="float-right" onClick={this.handleSignOut}>Log Out</Button>)
                        
                      } 
                    </ToolbarItem>
                  </Toolbar>
							</div>
					  </div>

            <div className="row">
              <div className="col-8">
                <StockChartContainer ticker={this.state.ticker} name={getName(this.state.ticker)}/>
						  </div>
              { (this.state.loggedIn === true &&
              <div className="col-4">
                <h3>My Stocks</h3>
								<MyStocksContainer ticker={this.state.ticker} name={getName(this.state.ticker)} handleTickerChange={this.handleTickerChange}/>
              </div>) 
              || (this.state.loggedIn === false &&
              <div className="col-4">
                <h3>About Saphire:</h3>
                < div className="memo">
                  <div className="stockName">
                    <img src={saphireLogo2} alt="Logo" width="175" height="175" />
                  </div>
                  <h5> 
                    &emsp;Saphire is a financial data center similar to Yahoo Finance or Google
                    Finance. Saphire provides graphics, statistics, and news about all the
                    Fortune 100 companies' allowing users to stay up-to-date on their
                    stocks. Additionally, Saphire uses artificial intelligence to predict
                    changes in prices, closing prices, and booms for companies. Join today
                    and make some money!
                  </h5>
                  <div className="stockName">
                    <h5>- Jewell Day, Lukas Jimenez-Smith,<br /> Brody Pearman, and Aaron Thompson </h5>
                  </div>
                </div>
              </div>
              )
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
							<SignInInput handleLoginStateChange = {this.handleLoginStateChange} handleRegistrationStateChange = {this.handleRegistrationStateChange} handleSuccessfulSignIn = {this.handleSuccessfulSignIn}/>
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
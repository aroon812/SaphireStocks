import React from "react";
import { Dialog, DialogActionsBar } from '@progress/kendo-react-dialogs';
import { Input } from '@progress/kendo-react-inputs'; 
import { Button, ButtonGroup, Toolbar, ToolbarItem } from '@progress/kendo-react-buttons';

export class SignInInput extends React.Component{
    constructor(props) {
        super(props);
        this.appContainer = React.createRef();
        this.state = {
          email: "",
          password: "",
          authtoken: ""
        }
      }

handleLogin = () => {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "POST", 'http://127.0.0.1:8000/api/api-token-auth/', false); // false for synchronous request
    xmlHttp.setRequestHeader("Content-Type","application/json");
    xmlHttp.send(JSON.stringify({ username: this.state.email, password: this.state.password }));
   
    if (xmlHttp.status===200){
      var json = JSON.parse(xmlHttp.responseText);
      this.setState({
        email: "",
        password: "",
      }, () => this.props.handleLoginStateChange());
      //localStorage.setItem("refreshToken", json['refresh']);
      //localStorage.setItem("accessToken", json['access']);
      localStorage.setItem("token", json['token']);
    }
  }
  
  handleLoginChange = event => {
    this.setState({ 
      [event.target.name]: event.target.value,
    })
  }
  
  render(){
  return (
    <Dialog title={"Sign In"} onClose={this.props.handleLoginStateChange}>             
        <div className="col">
        <div className="row">
            <p>Please enter your email and password.</p>
        </div>
    
        <div className="row justify-content-center">
            <Input label="Email" type="email" name="email" value={this.state.email} onChange={this.handleLoginChange} />
        </div>
        <div className="row justify-content-center">
            <Input label="Password" type="password" name="password" value={this.state.password} onChange={this.handleLoginChange} />                   
        </div>
        </div>

    <DialogActionsBar>
    <Button onClick={this.props.handleRegistrationStateChange}>Create Account</Button>
    <Button primary={true} onClick={this.handleLogin}>Sign In</Button>
    </DialogActionsBar>

    </Dialog>
  );
  }

}
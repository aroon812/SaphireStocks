import React from "react";
import { Dialog, DialogActionsBar } from '@progress/kendo-react-dialogs';
import { Input } from '@progress/kendo-react-inputs'; 
import { Button, ButtonGroup, Toolbar, ToolbarItem } from '@progress/kendo-react-buttons';

export class RegistrationInput extends React.Component{
    constructor(props) {
        super(props);
        this.appContainer = React.createRef();
        this.state = {
            fName: "",
            lName: "",
            email: "",
            password: "",
            confirm: ""
        }
    }

    handleRegisteration = () => {
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open("POST",'http://127.0.0.1:8000/api/users/', false);
        xmlHttp.setRequestHeader("Content-Type","application/json");
        xmlHttp.send(JSON.stringify({email: this.state.email}));
        
        var emailCheck = JSON.parse(xmlHttp.responseText);
        

    }

    handleRegistrationChange = event => {
        this.setState({ 
          [event.target.name]: event.target.value,
        })
      }

    render(){
        return(
            <Dialog title={"Create Account"} onClose={this.props.handleRegistrationStateChange}>
            <div className="col">
              <div className="row">
                <p>Please enter your first name, last name, email and new password.</p>
              </div>
              <div className="row justify-content-center">
                <Input label="First Name" type="text" name="fName" value={this.state.fName} onChange={this.handleRegisterationChange} />
              </div>
              <div className="row justify-content-center">
                <Input label="Last Name" type="text" name="lName" value={this.state.lName} onChange={this.handleRegistrationChange} />
              </div>
              <div className="row justify-content-center">
                <Input label="Email" type="email" name="email" value={this.state.email} onChange={this.handleRegistrationChange} />
              </div>
              <div className="row justify-content-center">
                <Input label="Password" type="password" name="password" value={this.state.password} onChange={this.handleRegistrationChange} />                   
              </div>
              <div className="row justify-content-center">
                <Input label="Confirm Password" type="password" name="confirm" value={this.state.password} onChange={this.handleRegistrationChange} />                   
              </div>
            </div>
          <DialogActionsBar>
            <Button onClick={this.props.handleRegistrationStateChange}>Cancel</Button>
            <Button primary={true} onClick={this.handleRegistration}>Create Account</Button>
          </DialogActionsBar>
        </Dialog>
        )
    }
}
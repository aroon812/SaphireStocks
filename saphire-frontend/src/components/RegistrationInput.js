import React from "react";
import { Dialog, DialogActionsBar } from '@progress/kendo-react-dialogs';
import { Input } from '@progress/kendo-react-inputs'; 
import { Button} from '@progress/kendo-react-buttons';


const validEmailRegex = RegExp(/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/);
const validateForm = (errors) => {
  let valid = true;
  Object.values(errors).forEach(
    (val) => val.length > 0 && (valid = false)
  );
  return valid;
}

export class RegistrationInput extends React.Component{
  constructor(props) {
    super(props);
    this.state = {
      fName: null,
      lName: null,
      email: null,
      password: null,
      confirm: null,
      errors: {
        fName: '',
        lName: '',
        email: '',
        password: '',
        confirm: '',
      }
    };
  }

  handleChange = (event) => {
    //event.preventDefault();
    const { name, value } = event.target;
    let errors = this.state.errors;

    switch (name) {
      case 'fName': 
        errors.fName = 
          value.length < 0
            ? 'First Name must be 1 characters long!'
            : '';
        break;
      case 'lName': 
        errors.lName = 
          value.length < 0
            ? 'Last Name must be 1 characters long!'
            : '';
        break;
      case 'email': 
        errors.email = 
          validEmailRegex.test(value)
            ? ''
            : 'Email is not valid!';
        break;
      case 'password': 
        errors.password = 
          value.length < 8
            ? 'Password must be 8 characters long!'
            : '';
        break;
      case 'confirm': 
         errors.confirm = 
          (value !== this.state.password)
            ? 'Passwords must match!'
            : '';
        break;
      default:
        break;
    }

    this.setState({errors, [name]: value}, () => console.log(this.state));

  }

  handleSubmit = (event) => {
    const errors = this.state;
    //event.preventDefault();
    if(validateForm(this.state.errors)) {
      var email = this.state.email.toLowerCase();
      console.info('Valid Form');
      var xmlHttp = new XMLHttpRequest();
      xmlHttp.open( "POST", 'http://129.114.16.219:8000/api/users/', false); // false for synchronous request
      xmlHttp.setRequestHeader("Content-Type","application/json");
      xmlHttp.send(JSON.stringify({ email: email, password: this.state.password, first_name: this.state.fName, last_name: this.state.lName }));
      

      if (xmlHttp.status===200){
        xmlHttp.open( "POST", 'http://129.114.16.219:8000/api/api-token-auth/', false); // false for synchronous request
        xmlHttp.setRequestHeader("Content-Type","application/json");
        xmlHttp.send(JSON.stringify({ username: this.state.email, password: this.state.password }));

        if (xmlHttp.status === 200){
          var json = JSON.parse(xmlHttp.responseText);

          this.setState({
            email: "",
            password: "",
          }, () => this.props.handleRegistrationStateChange());

          localStorage.setItem("token", json['token']);
        }
      }
    }else{
      errors.email = 'User with this email already exists!';//Lukas*
    }
  }

  render() {
    const {errors} = this.state;
      return (          
        <Dialog title={"Create Account"} onClose={this.props.handleRegistrationStateChange}>
        <div className="col">

          <div className="row">
            <div>
            <p>Please enter your first name, last name, email and new password.</p> <br/>
            {errors.fName.length > 0 && 
            <p className='error'>  {errors.fName}</p>}
            {errors.lName.length > 0 && 
            <p className='error'>  {errors.lName}</p>}
            {errors.email.length > 0 && 
            <p className='error'>  {errors.email}</p>}
            {errors.password.length > 0 && 
            <p className='error'>  {errors.password}</p>}
            {errors.confirm.length > 0 && 
            <p className='error'>  {errors.confirm}</p>}   
            </div>
          </div>

          <div className="row justify-content-center">
            <Input label='First Name' type="text" name="fName" onChange={this.handleChange} noValidate/>
          </div>

          <div className="row justify-content-center">
            <Input label='Last Name' type="text" name="lName" onChange={this.handleChange} noValidate/>
          </div>

          <div className="row justify-content-center">
            <Input label="Email" type="email" name="email" onChange={this.handleChange} noValidate/>
          </div>

          <div className="row justify-content-center">
            <Input label="Password" type="password" name="password" onChange={this.handleChange} noValidate/> 
          </div>

          <div className="row justify-content-center">
            <Input label="Confirm Password" type="password" name="confirm" onChange={this.handleChange} noValidate/>      
          </div>

        </div>
      <DialogActionsBar>
        <Button onClick={this.props.handleRegistrationStateChange}>Cancel</Button>
        <Button primary={true} onClick={this.handleSubmit}>Create Account</Button>
      </DialogActionsBar>
      </Dialog>
    );
  }
}


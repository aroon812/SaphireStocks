import React from "react";
import { Dialog, DialogActionsBar } from '@progress/kendo-react-dialogs';
import { Input } from '@progress/kendo-react-inputs'; 
import { Button, ButtonGroup, Toolbar, ToolbarItem } from '@progress/kendo-react-buttons';


const validEmailRegex = RegExp(/^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i);
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
    var match;
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
        match = (errors.confirm.localeCompare(errors.password))
         errors.confirm = 
          (this.state.confirm.length === this.state.password.length && match === 0)
            ? 'Passwords must match!'
            : '';
        break;
      default:
        break;
    }

    this.setState({errors, [name]: value});
  }

  handleSubmit = (event) => {
    //event.preventDefault();
    if(validateForm(this.state.errors)) {
      console.info('Valid Form')
    }else{
      console.error('Invalid Form')
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
            <p className='error'>  <br/>{errors.fName}</p>}

            {errors.lName.length > 0 && 
            <p className='error'>  <br/>{errors.lName}</p>}

            {errors.email.length > 0 && 
            <p className='error'>  <br/>{errors.email}</p>}

            {errors.password.length > 0 && 
            <p className='error'>  <br/>{errors.password}</p>}

            {errors.confirm.length > 0 && 
            <p className='error'>  <br/>{errors.confirm}</p>}   
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
        <Button primary={true} onClick={this.handleRegistration}>Create Account</Button>
      </DialogActionsBar>
      </Dialog>
    );
  }
}


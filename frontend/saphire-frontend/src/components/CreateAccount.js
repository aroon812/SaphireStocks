import React from 'react';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';

import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import { authLogin, authFail } from '../store/authActions';
import { connect } from 'react-redux';

import * as actions from '../store/authActions';
import axios from 'axios';

import * as settings from '../settings';

import { useHistory, useLocation } from "react-router-dom";

const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

function CreateAccount(props) {
  const classes = useStyles();
  const [username, setuserName] = React.useState(null);
  const [password, setPassword] = React.useState(null);
  const [password_confirmation, setPasswordConfirmation] = React.useState(null);

  let history = useHistory();
  let location = useLocation();
  let { from } = location.state || { from: { pathname: "/"} };

  const handleFormFieldChange = (event) => {
    switch (event.target.id) {
      case 'username': setuserName(event.target.value); break;
      case 'password': setPassword(event.target.value); break;
      case 'password_confirmation': setPasswordConfirmation(event.target.value); break;
      default: return null;
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post(`${settings.API_SERVER}/api/auth/users/`, {
        email: username,
        password: password
    })
    .then(res => {
        history.push('/login/') 
    })
    .catch(err => {
        alert(err.response.data.message);
    });
  }

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>
        <Avatar className={classes.avatar}>
          <LockOutlinedIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          Create Account
        </Typography>
        <form className={classes.form} noValidate onSubmit={handleSubmit}>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="username"
            label="Email"
            name="username"
            autoComplete="username"
            autoFocus
            onChange={handleFormFieldChange}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
            onChange={handleFormFieldChange}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="password_confirmation"
            label="Enter Your Password Again"
            type="password"
            id="password_confirmation"
            onChange={handleFormFieldChange}
            error={password !== password_confirmation}
            helperText={password !== password_confirmation ? "Passwords don't match" : null}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}
          >
            Create Account
          </Button>
        </form>
      </div>
    </Container>
  );
}

export default CreateAccount;
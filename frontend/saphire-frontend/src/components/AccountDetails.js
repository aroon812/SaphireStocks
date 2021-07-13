import React, { useEffect } from 'react';
import axios from 'axios';
import * as settings from '../settings';

import { makeStyles } from '@material-ui/core/styles';
import { Avatar, Button, Container, CssBaseline, TextField, Typography } from '@material-ui/core';
import VpnKeyIcon from '@material-ui/icons/VpnKey';

import { connect } from 'react-redux';
import * as actions from '../store/authActions';

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
    backgroundColor: theme.palette.success.main,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
  success: {
      color: theme.palette.success.main,
  }
}));

function AccountDetails(props) {

  useEffect(() => {
    let headers = {'Authorization': `Token ${props.token}`};
    let method = 'get';
    let url = settings.API_SERVER + '/api/auth/users/current_user/';
    let config = { headers, method, url};

    axios(config).then(res => {
      setEmail(res.data["email"])
    }).catch(
        error => {
            alert(error)
        })
  }, [])

  const classes = useStyles();
  const [account_email, setEmail] = React.useState("");
  const [success, setSuccess] = React.useState(false);

  const handleFormFieldChange = (event) => {
    setSuccess(false);
    switch (event.target.id) {
      case 'email': setEmail(event.target.value); break;
      default: return null;
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    let headers = {'Authorization': `Token ${props.token}`};
    let method = 'patch';
    let url = settings.API_SERVER + '/api/auth/users/current_user/';
    let accountFormData = new FormData();
    accountFormData.append("email", account_email);
    let config = { headers, method, url, data: accountFormData};

    axios(config).then(res => {
        setSuccess(true);
    }).catch(
        error => {
            alert(error)
        })
    
    }

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>
        {success ? <Typography variant="button" className={classes.success} gutterBottom>Account Details Updated!</Typography> : null}
        <Avatar className={classes.avatar}>
          <VpnKeyIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          My Account
        </Typography>
        <form className={classes.form} noValidate onSubmit={handleSubmit}>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="email"
            label="Email"
            value={account_email}
            type="text"
            id="email"
            onChange={handleFormFieldChange}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}
          >
            Update Account Details
          </Button>
          <Button color="inherit" href="/update_password">
              Update Password
          </Button>
        </form>
      </div>
    </Container>
  );
}

export default AccountDetails;
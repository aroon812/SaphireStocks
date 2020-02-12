import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

import { BrowserRouter as Router, Route, Link } from "react-router-dom";

import Stock from "./Component/Stock/index";

class App extends Component {
  render() {
    return (
      <Router>
        <Route path="/" exact component={Stock} />
    </Router>
    );
  }
}

export default App;
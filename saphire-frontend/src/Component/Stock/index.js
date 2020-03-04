import React, { Component } from "react";

import axios from "axios";

export default class Stock extends Component {
  constructor(props) {
    super(props);
    this.state = {
    stocks:[],
    };
    this.loadStocks = this.loadStocks.bind(this);
  }

  componentWillMount() {
    this.loadStocks();
  }

  async loadStocks()
  {
    const promise = await axios.get("http://localhost:8000/api/stocks");
    const status = promise.status;
    if(status===200)
    {
      const data = promise.data.data;
      this.setState({stocks:data});
    }
  }

  render() {
    return(
      <div>
        <h1>Stocks</h1>
            {this.state.stocks}
            
      </div>
    )
  }
}
//.map((value,index)=>{return <h4 key={index}>{value}</h4> )}
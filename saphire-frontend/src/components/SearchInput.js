import { Input } from '@progress/kendo-react-inputs'; 
import React from 'react';
import {getCompanyData} from '../data/appData';
import { Button, ToolbarItem } from '@progress/kendo-react-buttons';




export class SearchInput extends React.Component {
  constructor(props){
    super(props);
    this.state = {
        data: {
          search: "",
          cName: "",
          cTicker: "",
          errors: "",
        },
        query: "",
      }
  }

  search = (query) => {
    var searchResults = getCompanyData(query);
    this.props.callback(searchResults);
  }

  handleInput = (event) => {
      this.search(this.state.query);
  }

  handleQueryChange = event => {
    this.setState({ 
      [event.target.name]: event.target.value,
    });
  }

  render() {
    return (
      <ToolbarItem className="float-right d-flex">
        <Input label="Search..." name="query" value={this.state.query} onChange={this.handleQueryChange}/>
        <Button className="float-right" onClick={this.handleInput}>Search</Button> 
      </ToolbarItem>
    );
  }
}






import { Input } from '@progress/kendo-react-inputs'; 
import React from 'react';
import {getCompanyData} from '../data/appData';
import { Button, ButtonGroup, Toolbar, ToolbarItem } from '@progress/kendo-react-buttons';

export class SearchInput extends React.Component {
    constructor(props){
      super(props);
      this.state = {
        query: "",
        data: [],
        filteredData: []
      }
    }
  /*
    handleQueryChange = event => {
      const query = event.target.value;
  
      this.setState(prevState => {
        const filteredData = prevState.data.filter(element => {
          return element.name.toLowerCase().includes(query.toLowerCase());
        });
  
        return {
          query,
          filteredData
        };
      });
    };
    <div>{this.state.filteredData.map(i => <p>{i.name}</p>)}</div>
*/
    
    handleQueryChange = event => {
      console.log(event);
      this.setState({ 
        [event.target.name]: event.target.value,
      }, () => console.log(this.state.query));
    }

    handleSearch = () => {
      getCompanyData(this.state.query);
    }

    render() {
      return(
        <div>
          <Toolbar>
          <ToolbarItem>
          <Input label="Search..." name="query" value={this.state.query} onChange={this.handleQueryChange}/>
          </ToolbarItem>
          <ToolbarItem>
          <Button className="float-right" onClick={this.handleSearch}>Search</Button> 
          </ToolbarItem>
          
          </Toolbar>
        </div>
      )
    }
  }
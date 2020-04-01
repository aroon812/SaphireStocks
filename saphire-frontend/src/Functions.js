
export const handlePDFExport = () => {
    savePDF(ReactDOM.findDOMNode(this.appContainer), { paperSize: 'auto' });
  }

export const handleShare = () => {
    this.setState({
      showDialog: !this.state.showDialog
    }, () => console.log(this.state))
  }

export const handleLogin = () => {
    this.setState({ 
        showLogin: !this.state.showLogin
    }, () => console.log(this.state))
    }

export const handleRegistration = () => {
    this.setState({
      showResgistration: !this.state.showResgistration
    }, () => console.log(this.state))
  }

  
export const handleSelect = (e) => {
      this.setState({selected: e.selected})
  }

export const Header4 = (text) => (
    <h4>{text}</h4>
  )
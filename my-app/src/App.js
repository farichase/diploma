import logo from './logo4.png';
import './App.css';
import CodeEditor from './Components/CodeEditor/CodeEditor.jsx';
import Buttons from './Components/Buttons/Buttons.jsx';
import OutputAreaCode from './Components/OutputAreaCode/OutputAreaCode.jsx';
import React, { Component } from 'react'
import Lines from './Lines/Lines';
import DataBase from './Components/CodeEditor/DataBase/DataBase';


class App extends Component {
  state = {
    enteringCode: "",
    result: "",
    suggestFrame: [],
    lines: 0
  }
  changeResult = async (code) => {
    this.setState({
      result: code
    })
  }
  changeEnteringCode = async(code) => {
    this.setState({
      enteringCode: code
    })
  }
  suggest = async() =>{
    const stdout = await fetch('http://localhost:8080/syntaxCompletions/exec', {
			method: 'POST',
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				data: this.state.enteringCode
			})
		}).then(res => {
			if (res.ok) {
				return res.json()
			}
		})
    let stdoutData = await stdout
    this.setState({suggestFrame : stdoutData.data})
    // console.log(stdoutData.data)
  }
  changeLines = async(lines) =>{
    this.setState({
      lines: lines
    })
  }
  render () {
    return(
      <div className = "App" >
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <Buttons changeResult={this.changeResult} enteringCode={this.state.enteringCode} result={this.state.result}/>
        </header>

        <div className="bar">

          <Lines lines={this.state.lines}/>
          <CodeEditor changeLines={this.changeLines} changeEnteringCode={this.changeEnteringCode} suggest={this.suggest} suggestFrame={this.state.suggestFrame}/>
          <OutputAreaCode result={this.state.result}/>
        </div>
      </div>
    )
  }
  
}
export default App;

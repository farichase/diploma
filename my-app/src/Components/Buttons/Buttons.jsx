import './Buttons.css'
import React, { Component } from 'react'
import Button from './Button/Button.jsx'
import DataBase from '../CodeEditor/DataBase/DataBase'

class Buttons extends Component {
	state = {
		fileFormats: ["ref", "dot"],
		selectedFileFormat: "ref",
		compilerVersions: ["SCP4", "MSCP-A"],
		selectedCompilerVersion: "SCP4",
		isFileAdded: false,
		emptyList: []
	}
	setFileFormat = async(fileFormat) => {
		this.setState({
			selectedFileFormat : fileFormat,
		})
	}
	setCompilerVersion = async(version) => {
		this.setState({
			selectedCompilerVersion : version,
		})
	}
	changeStatusAboutFileAdding = async(val) => {
		this.setState({
			isFileAdded: val
		})
	}
	render() {
		return (
			<div className="buttons">

				<Button name="Add a file" 
						list={this.state.emptyList}
						isFileAdded={this.state.isFileAdded}
						changeStatusAboutFileAdding={this.changeStatusAboutFileAdding}
						changeResult={this.props.changeResult}/>
				<Button name="Supercompiler version" 
						list={this.state.compilerVersions} 
						setCompilerVersion={this.setCompilerVersion}
						selectedFileFormat={this.state.selectedFileFormat}/>		
				<Button name="Output file format" 
						list={this.state.fileFormats} 
						setFileFormat={this.setFileFormat}
						selectedCompilerVersion={this.state.selectedCompilerVersion} />		
				<Button name="Transform" list={this.state.emptyList} 
						changeResult={this.props.changeResult} 
				        isFileAdded={this.state.isFileAdded}
						changeStatusAboutFileAdding={this.changeStatusAboutFileAdding}
						enteringCode={this.props.enteringCode}
						selectedCompilerVersion={this.state.selectedCompilerVersion} 
						selectedFileFormat={this.state.selectedFileFormat}/>
				<Button name="Download result" list={this.state.emptyList}
						selectedCompilerVersion={this.state.selectedCompilerVersion}
						selectedFileFormat={this.state.selectedFileFormat}
						result={this.props.result}
						/>
			</div>
		)
	}
}

export default Buttons

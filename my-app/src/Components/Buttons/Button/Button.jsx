import './Button.css'
import React, { Component } from 'react'

class Button extends Component {
	state = {
		button: "",
		name: "",
		newName: "", 
	}
	componentDidMount(){
		if (this.props.list[0]){
			this.setState({
				button: this.props.name,
				name: this.props.name + ": " + this.props.list[0],
				newName: this.props.name + ": " + this.props.list[0]
			})
		} else {
				this.setState({
					button: this.props.name,
					name: this.props.name,
					newName: this.props.name
				})
		} 
	}
	changeName = async(item) => {
		if (this.state.name.includes("Supercompiler version")){
			this.props.setCompilerVersion(item)
			this.setState({
				newName: this.state.button + ": " + item 
			})
		} 
		if (this.state.name.includes("Output file format")){
			this.props.setFileFormat(item)
			this.setState({
				newName: this.state.button + ": " + item 
			})
		} 
    }
	handleFile = async(e) => {
		const content = e.target.result;
		fetch('http://localhost:8080/files/upload', {
			method: 'POST',
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				content: content
			})
		}).then(res => {
			if (res.ok) {
				return res.json()
			}
		})

	}
	loadFile = async() => {
		const input = document.createElement("input")
		input.type = "file"
		input.name = "file"
		input.style.display = "none"
		input.accept = ".ref,.smt" 
		document.body.appendChild(input)
		input.click()
		input.onchange = async () => {
			const file = input.files?.item(0)
			if (!file) return
			let fileData = new FileReader();
  			fileData.onloadend = this.handleFile;
  			fileData.readAsText(file);
			document.body.removeChild(input)
		}
		this.props.changeStatusAboutFileAdding(true)
		this.props.changeResult("File added")
	}
	transformFile = async() => {
		this.props.changeResult("")	
		if (!this.props.isFileAdded) this.enterCode()
		this.props.changeStatusAboutFileAdding(false)
		const res = await fetch('http://localhost:8080/files/transform', {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
				compilerVersion: this.props.selectedCompilerVersion,
				fileFormat: this.props.selectedFileFormat
			}),
        }).then(res => {
			if (res.ok){
				return res.json()
			}
		})

		this.props.changeResult(res.data)	
		if (this.props.selectedCompilerVersion == "MSCP-A" && this.props.selectedFileFormat == "dot") {
			console.log("true")
			const res2 = await fetch('http://localhost:8080/files/graph', {
				method: 'POST',
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({
					data: ""
				}),
			}).then(res => {
				if (res.ok){
					return res.json()
				}
			})
			console.log(res2.data)
			this.props.changeResult(res2.data)	
		
		}
	
		
		
	}
	
	downloadData = async() => {		
		if (this.props.selectedFileFormat === "ref") {
			const fileContent = this.props.result
			let filename = "result.ref"
			let element = document.createElement('a');
			element.setAttribute('href', 'data:application/ref;charset=utf-8,' + encodeURIComponent(fileContent));
			element.setAttribute('download', filename);
			element.style.display = 'none';
			document.body.appendChild(element);
			element.click();
			document.body.removeChild(element);
		} 
	}
	enterCode = async() => {
		let content = this.props.enteringCode;
		if (this.props.selectedCompilerVersion === 'SCP4' && this.props.selectedFileFormat === 'ref') {
			content = '*$MST_FROM_ENTRY;\n' + content
		}
		fetch('http://localhost:8080/files/upload', {
			method: 'POST',
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				content: content
			})
		}).then(res => {
			if (res.ok) {
				return res.json()
			}
		})
	}
	findOutTypeOfFunction = async() => {
		if (this.state.newName === "Add a file") {
			this.loadFile()
		}
		if (this.state.newName === "Transform") {
			this.transformFile()
		}
		if (this.state.newName === "Download result") {
			this.downloadData()
		}
	}
	render() {
		let list = ""
		if (this.props.name.includes("Output")){
			if (this.props.selectedCompilerVersion === "SCP4") {
				list = ["ref"]
			} else {
				list = ["ref", "dot"]
			}
		}
		if (this.props.name.includes("Supercompiler")){
			if (this.props.selectedFileFormat === "dot") {
				list = ["MSCP-A"]
			} else {
				list = ["SCP4", "MSCP-A"]
			}
		}
		return (
			<div className="buttonClass">
				<button className="nameButton" onClick={this.findOutTypeOfFunction}>{this.state.newName}</button>
				<div className="dropdown-content">
				{
					list.length !== 0 && (
						list.map(item => {
							return (
								<button className="item" key={item} onClick={this.changeName.bind(this, item)}>{item}</button>
							)
						})
					)
				}
				</div>
			</div>
		)
	}
}

export default Button

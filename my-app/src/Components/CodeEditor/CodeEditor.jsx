import './CodeEditor.css'
import React, { Component } from 'react'
import SuggestFrame from './SuggestFrame/SuggestFrame'
import DataBase from './DataBase/DataBase'
import Lines from '../../Lines/Lines'
import { ScrollSync } from 'react-scroll-sync'
import { ScrollSyncPane } from 'react-scroll-sync'


class CodeEditor extends Component {
	state = {
		firstKey: 0,
		value: "",
	}
	componentDidMount() {
		this.setState({
			n: 0
		})
	}
	calculateCells = async (text) => {
		this.setState({
			value: text
		})
		let lines = text.split(/\r|\r\n|\n/);
		let count = lines.length;
		this.setState({
			count: count
		})
		this.props.changeLines(count)

	}

	handleChange = async (event) => {
		let text = event.target.value
		this.calculateCells(text)
		this.props.changeEnteringCode(text)
	}
	// handleKeyDown = async (e) => {
	// 	if (e.keyCode === 17) {
	// 		if (this.state.firstKey === 20) {
	// 			this.props.suggest()
	// 			this.setState({ firstKey: 0 });
	// 		} else {
	// 			this.setState({ firstKey: 17 });
	// 		}
	// 	}
	// 	if (e.keyCode === 20) {
	// 		if (this.state.firstKey === 17) {
	// 			this.props.suggest()
	// 			this.setState({ firstKey: 0 });
	// 		} else {
	// 			this.setState({ firstKey: 20 });
	// 		}
	// 	}

	// }
	changeValue = (val) => {
		this.setState({
			value: val
		})
		this.calculateCells(val)
		this.props.changeEnteringCode(val)
	}
	render() {
		let stdout = this.props.suggestFrame

		return (
			<div className="CodeEditorClass">
				<textarea className="CodeEditor" value={this.state.value} onKeyDown={this.handleKeyDown} id="CodeEditor" onChange={this.handleChange} wrap="off" autoCapitalize="off" spellCheck="false" ></textarea>
				<DataBase changeValue={this.changeValue} />
				{/* {
					stdout.length !== 0 &&
					<div className='Suggest'>
						<SuggestFrame valuesArray={stdout} />
					</div>
				} */}
			</div>
		)
	}
}

export default CodeEditor

import './Lines.css'
import React, { Component } from 'react'

class Lines extends Component {

	render() {
		let cells = Array(this.props.lines).fill().map((e, i) => i + 1)
		return (
			<div className="Lines" id="tb2">
				{
					<div>{cells.map(item => <div key={item} className="val">{item}</div>)}</div>
				}
			</div>
		)
	}
}

export default Lines

import './OutputAreaCode.css'
import React, { useState } from 'react'
import image from './img.png';


const OutputAreaCode = ({ result }) => {
	const [pos, setPos] = useState({ x: 0, y: 0, scale: 1 });

	const onScroll = (e) => {
		const delta = e.deltaY * -0.01;
		const newScale = pos.scale + delta;

		const ratio = 1 - newScale / pos.scale;

		setPos({
			scale: newScale,
			x: pos.x * ratio,
			y: pos.y * ratio
		});
	};
	console.log(result)
	return (
		<div className="OutputAreaCodeClass">
			{
				result === "stdout" &&
				<div className="img-wrapper" onWheelCapture={onScroll}>
					<img src={image} alt="" className="hover-zoom"
						style={{
							transformOrigin: "0 0",
							transform: `translate(${pos.x}px, ${pos.y}px) scale(${pos.scale})`
						}} />
				</div> 
			}
			{
				result === "It is impossible to build a graph" && <textarea className="OutputAreaCode" wrap="soft" disabled={true} value={"It is impossible to build a graph"}></textarea>
			}
			{
				result !== "" && result !== "It is impossible to build a graph" && result !== "stdout" && <textarea className="OutputAreaCode" wrap="soft" disabled={true} value={result}></textarea>
			}
		</div>
	)
}


export default OutputAreaCode
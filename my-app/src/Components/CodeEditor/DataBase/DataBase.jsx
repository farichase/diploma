import React, { useState } from 'react'

import './DataBase.css'

const DataBase = ({changeValue}) => {
    const [open, setIsOpen] = useState(false);
    const openForm = () => setIsOpen(true);
    const closeForm = () => setIsOpen(false);
    const loadFile = async (e) => {
        const readFile = await fetch('http://localhost:8080/tests/load', {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                file: e
            })
        }).then(res => {
            if (res.ok) {
                return res.json()
            }
        })
        let file = await readFile.data;
        changeValue(file)
        closeForm()
    }
    return (
        <div className="database">
          
            <div>
                <button className="openButton" onClick={openForm}>Open tests</button>
                {
                    open &&
                    <div className="chatPopup" id="myForm" >
                        <div className="formContainer" >
                            <button className="btn" onClick={(e) => loadFile(e.target.innerText)}>input1.ref</button>
                            <button className="btn" onClick={(e) => loadFile(e.target.innerText)}>input2.ref</button>
                            <button className="btn" onClick={(e) => loadFile(e.target.innerText)}>input3.ref</button>
                            <button className="btn" onClick={(e) => loadFile(e.target.innerText)}>input4.ref</button>
                            <button className="btn" onClick={(e) => loadFile(e.target.innerText)}>input5.ref</button>
                            <button className="btn" onClick={(e) => loadFile(e.target.innerText)}>input6.ref</button>
                            <button className="btn" onClick={(e) => loadFile(e.target.innerText)}>input7.ref</button>
                            <button className="btn" onClick={(e) => loadFile(e.target.innerText)}>input8.ref</button>
                            <button className="btn" onClick={(e) => loadFile(e.target.innerText)}>input9.ref</button>

                            <button className="openButton" onClick={closeForm}>Close</button>
                        </div>
                    </div>
                }
            </div>
        </div>
    )
}

export default DataBase
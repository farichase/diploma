import './SuggestFrame.css'
const SuggestFrame = ({valuesArray}) => {
    return (
        <>
            {
                valuesArray.length !== 0 && valuesArray.split('\n').map(val => 
                    <div className='value'>
                        {val}
                    </div>
                )
            }
        </>
    );
}


export default SuggestFrame;
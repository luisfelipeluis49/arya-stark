import React, { useState } from 'react';

const Input = ({ label, value }) => {
    const [inputValue, setInputValue] = useState(value);

    const handleChange = (e) => {
        setInputValue(e.target.value);
    };

    return (
        <div>
            <label>{ label }</label>
            <input type="text" value={inputValue} onChange={ handleChange } />
        </div>
    );
};

export default Input;
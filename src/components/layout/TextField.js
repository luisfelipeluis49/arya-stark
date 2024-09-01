import React from 'react';

const TextField = ( { value } ) => {
    const textFieldStyle = {
        backgroundColor: '#F7F9FA',
        border: '1px solid grey'
    };

    return (
        <input type="text" readOnly style={textFieldStyle} value={ value }/>
    );
};

export default TextField;
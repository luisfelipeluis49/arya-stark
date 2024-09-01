import React from 'react';
import PropTypes from 'prop-types';

const Button = ( { text, type, width, onClick } ) =>
    {
    const buttonStyle =
    {
        backgroundColor: type === 'primary' ? 'blue' : 'white',
        color: type === 'primary' ? 'white' : 'blue',
        border: `1px solid blue`,
        width: width === '100%' ? '100%' : '90px',
        padding: '10px',
        borderRadius: '5px',
        cursor: 'pointer',
    };

    return (
        <button
            style={ buttonStyle }
            onClick={ onClick }>
            {text}
        </button>
    );
};

Button.propTypes = {
    text: PropTypes.string.isRequired,
    type: PropTypes.oneOf( ['primary', 'secondary'] ).isRequired,
    width: PropTypes.oneOf( ['100%', '90px'] ).isRequired,
    onClick: PropTypes.func.isRequired
};

export default Button;
import React from 'react';
import PropTypes from 'prop-types';

const Title = ( { text } ) =>
{
    return (
        <h2
            style=
            {
                {
                    fontSize: '24px',
                    fontWeight: 'light'
                }
            }
        >
            { text }
        </h2>
    );
};

Title.propTypes = {
    text: PropTypes.string.isRequired,
};

export default Title;
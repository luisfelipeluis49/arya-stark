import React from 'react';
import PropTypes from 'prop-types';

const Card = ( { title, svg } ) =>
{
    return (
        <div
            className="card"
            title={ title }
        >
            <svg className="login-icon" viewBox="0 0 24 24">
                { svg }
            </svg>
        </div>
    );
};

Card.propTypes =
{
    title: PropTypes.string.isRequired,
    svg: PropTypes.element.isRequired
};

export default Card;
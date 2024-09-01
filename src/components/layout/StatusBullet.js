import React from 'react';
import PropTypes from 'prop-types';

const StatusBullet = ( { color } ) =>
{
    return (
        <div
            style={{
                width: '15px',
                height: '15px',
                borderRadius: '50%',
                backgroundColor: color,
            }}
        />
    );
};

StatusBullet.propTypes = {
    color: PropTypes.string.isRequired,
};

export default StatusBullet;
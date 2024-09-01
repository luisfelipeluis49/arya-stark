import React from 'react';
import PropTypes from 'prop-types';

const FAB = ( { icon, onClick } ) =>
{
    return (
        <button
            style=
            {
                {
                    width: '56px',
                    height: '56px',
                    borderRadius: '50%',
                    backgroundColor: 'white',
                    border: '1px solid gray',
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                }
            }
            onClick={ onClick }
        >
            <svg
                className="w-6 h-6 text-white mr-2"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
            >
                { icon }
            </svg>
        </button>
    );
};

FAB.propTypes =
{
    icon: PropTypes.element.isRequired,
    onClick: PropTypes.func.isRequired
};

export default FAB;
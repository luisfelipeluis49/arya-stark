import React from 'react';

const Banner = ( { title, description } ) =>
{
    return (
        <div
            style=
            {
                {
                    width: '100%',
                    border: '1px solid gray',
                    backgroundColor: '#F7F9FA',
                    padding: '10px',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '10px'
                }
            }
        >
            <h1
                style=
                {
                    {
                        fontFamily: 'light',
                        fontSize: '36px',
                        color: '#000000'
                    }
                }
            >
                { title }
            </h1>
            <p
                style=
                {
                    {
                        fontFamily: 'light',
                        fontSize: '18px',
                        color: '#637282'
                    }
                }
            >
                { description }
            </p>
        </div>
    );
};

export default Banner;
import React from 'react';

const Policy = ( policy, onClick ) => {
    return (
        <div>
            <div>
                <h2>{ policy.title }</h2>
                <i
                    style={{ fontSize: '50px' }}
                    onClick={ onClick }
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        onClick={ onClick }
                    >
                        <path d="M12 19l7-7 3 3-7 7-3-3z" />
                        <path d="M10 3h4v12h-4z" />
                    </svg>
                </i>
            </div>
            <div
                style={{
                    width: '100%',
                    border: '1px solid gray',
                    padding: '10px',
                    borderRadius: '10px',
                    color: 'gray'
                }}
            >
                { policy.description }
            </div>
        </div>
    );
};

export default Policy;
import React from 'react';

const Dialog = ({ children }) => {
    return (
        <div className="dialog-container">
            <div className="dialog-backdrop"></div>
            <div className="dialog-content">
                {children}
            </div>
        </div>
    );
};

export default Dialog;
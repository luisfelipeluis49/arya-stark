import React from 'react';

const OptionsSidebar = ( { children } ) =>
{
    const sidebarStyle =
    {
        width: '200px',
        height: '100%',
        backgroundColor: 'transparent',
        display: 'flex',
        flexDirection: 'column',
        gap: '10px',
        overflowY: 'auto'
    };

    return (
        <div style={ sidebarStyle }>
            { children }
        </div>
    );
};

export default OptionsSidebar;
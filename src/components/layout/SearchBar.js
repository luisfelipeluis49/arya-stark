import React from 'react';

const SearchBar = ( clientArray, setClientArray ) =>
{
    const unfilteredArray = clientArray;

    const handleSearch = ( searchTerm ) =>
    {
        if ( !searchTerm || searchTerm === '' )
        {
            setClientArray( unfilteredArray );
            return;
        }

        const tempArray = clientArray.filter(
            ( client ) =>
            {
                return client.name.toLowerCase()
                                  .includes( searchTerm.toLowerCase() );
            }
        );

        setClientArray( tempArray );
    };

    return (
        <input
            type="text"
            placeholder="Search..."
            onChange={ handleSearch }
        />
    );
};

export default SearchBar;
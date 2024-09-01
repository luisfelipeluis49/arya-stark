import React from 'react';
import PropTypes from 'prop-types';
import BigClientCard from './BigClientCard';

const BigCardList = ( { clientArray } ) =>
{
    return (
        <div
            style=
            {
                {
                    display: 'flex',
                    flexWrap: 'wrap',
                    overflow: 'auto'
                }
            }
        >
            {
                clientArray.map( ( client, index ) =>
                    (
                        <BigClientCard
                            key={ index }
                            client={ client }
                            style=
                            {
                                {
                                    flex: '0 0 33.33%',
                                    maxWidth: '33.33%'
                                }
                            }
                        />
                    )
                )
            }
        </div>
    );
};

BigCardList.propTypes =
{
    clientArray: PropTypes.arrayOf( PropTypes.object ).isRequired,
};

export default BigCardList;

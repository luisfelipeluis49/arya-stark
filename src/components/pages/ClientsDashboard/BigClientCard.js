import React from 'react';
import PropTypes from 'prop-types';
import Link from 'next/link';
import Card from '../../layout/Card';

const SideClientCard = ( { client } ) =>
{
    return (
        <Link href={ `/clients/${ client.id }` }>
            <h3>{ client.title }</h3>
            <div className='colorCard'>
                <Card
                    title={ client.title }
                    svg={ client.logo }
                />
            </div>
        </Link>
        
    );
};

SideClientCard.propTypes =
{
    client: PropTypes.object.isRequired,
};

export default SideClientCard;
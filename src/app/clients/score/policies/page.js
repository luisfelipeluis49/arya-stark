'use client'

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import MenuSidebar from '@/components/layout/MenuSidebar';
import OptionsSidebar from '@/components/layout/OptionsSidebar';
import Title from '@/components/layout/Title';
import Banner from '@/components/layout/Banner';
import PoliticDialog from '@/components/dialog/PoliticDialog';
import Button from '@/components/layout/Button';
import Policy from '@/components/pages/ClientScorePolicies/Policy';

const Page = () =>
{
    const router = useRouter();

    const [ data, setData ] = useState( null );
    const [ isLoading, setLoading ] = useState( true );
    const [ showModal, setShowModal ] = useState( false );

    const handleNewCma = async ( cmaRules ) =>
    {
        try
        {
            const response =
                await fetch( 'http://localhost:8000/api/policies',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify( { cmaRules } )
                } );

            if ( response.ok )
            {
                const data = await response.json();
                router.push(
                    {
                        pahtname: `/clients/report/${ data.slug }`,
                        query: { data: data }
                    }
                );
            }
        }
        catch ( error )
        {
            console.error( error );
        }
    };

    useEffect( () =>
    {
        fetch( `http://localhost:8000/api/policies` )
            .then( ( response ) => response.json() )
            .then( ( data ) =>
            {
                setData( data );
                setLoading( false );
            } );
    }, [] );

    if ( isLoading )
    {
        return <h1>Loading...</h1>;
    }

    if ( !data )
    {
        return <h1>Policies not found</h1>;
    }

    const openModal = () =>
    {
        setShowModal( true );
    };

    const closeModal = () =>
    {
        setShowModal( false );
    };

    return (
        <div
            style=
            {
                {
                    display: 'flex',
                    flexDirection: 'row',
                    height: '100%'
                }
            }
        >
            <MenuSidebar />
            <div
                style=
                {
                    {
                        flex: 1,
                        display: 'flex',
                        flexDirection: 'column'
                    }
                }
            >
                <div
                    style=
                    {
                        {
                            display: 'flex',
                            justifyContent: 'space-between'
                        }
                    }
                >
                    <Title text="Page Title" />
                </div>
                <Banner title="Welcome" description="This is the page banner" />
                <div style={{ overflowY: 'scroll', flex: 1 }}>
                    {
                        data.policies.map((policy, index) =>
                            (
                                <Policy
                                    key={ index }
                                    policy={ policy }
                                    onClick={ openModal }
                                />
                            )
                        )
                    }
                </div>
                <Button
                    text='Add policy'
                    type='Secondary'
                    width='100%'
                    onClick={ openModal }
                />
                <Button
                    text='Save policies'
                    type='primary'
                    width='100%'
                    onClick={ () => handleNewCma( data.cmaRules ) }
                />
            </div>
            <OptionsSidebar>
            </OptionsSidebar>
            { showModal && <PoliticDialog closeModal={ closeModal } /> }
        </div>
    );
};

export default Page;
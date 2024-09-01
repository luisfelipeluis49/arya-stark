'use client'

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import MenuSidebar from '@/components/layout/MenuSidebar';
import OptionsSidebar from '@/components/layout/OptionsSidebar';
import Title from '@/components/layout/Title';
import Banner from '@/components/layout/Banner';
import Button from '@/components/layout/Button';
import AnalysisPoint from '@/components/pages/ClientScoreReport/AnalysisPoint';

const Page = ( { params } ) =>
{
    const router = useRouter();

    const [ data, setData ] = useState( null );
    const [ isLoading, setLoading ] = useState( true );

    const handleAnalyze = async ( cnpj ) =>
    {
        try
        {
            const response =
                await fetch( 'http://localhost:8000/analyze',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify( { cnpj: cnpj } )
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
        fetch( `http://localhost:8000/analyze/${ params.cnpj }`, { mode: 'no-cors'} )
            .then( ( response ) => response.json() )
            .then( ( data ) =>
            {
                setData( data );
                setLoading( false );
            } );
    }, [ params.cnpj ] );

    if ( isLoading )
    {
        return <h1>Loading...</h1>;
    }

    if ( !data )
    {
        return <h1>Client not found</h1>;
    }

    return (
        <div
            style={{
                display: 'flex',
                flexDirection: 'row',
                height: '100%',
            }}
        >
            <MenuSidebar />
            <div
                style={{
                    flex: 1,
                    display: 'flex',
                    flexDirection: 'column',
                }}
            >
                <div
                    style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                    }}
                >
                    <Title text="Page Title" />
                </div>
                <Banner title="Welcome" description="This is the page banner" />
                <div
                    style={{
                        display: 'flex',
                        flexDirection: 'row',
                        flexWrap: 'wrap',
                        justifyContent: 'space-between',
                        overflow: 'hidden',
                    }}
                >
                    {
                        data.riskAnalysisPoint.map(
                            ( item, index ) =>
                            (
                                <div
                                    style={{
                                        flexBasis: '50%',
                                        marginBottom: '20px'
                                    }}
                                    key={ index }>
                                    <AnalysisPoint item={ item } />
                                </div>
                            )
                        )
                    }
                </div>
            </div>
            <OptionsSidebar>
                <Button
                    text="Run again"
                    type="primary"
                    width="90"
                    onClick={ handleAnalyze }
                />
                <Button
                    text="Client account"
                    type="secondary"
                    width="90"
                    onClick={ () => router.push('/clients') }
                />
            </OptionsSidebar>
        </div>
    );
};

export default Page;
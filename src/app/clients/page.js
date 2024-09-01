'use client'

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import MenuSidebar from '@/components/layout/MenuSidebar';
import OptionsSidebar from '@/components/layout/OptionsSidebar';
import Title from '@/components/layout/Title';
import SearchBar from '@/components/layout/SearchBar';
import Banner from '@/components/layout/Banner';
import BigCardList from '@/components/pages/ClientsDashboard/BigCardList';
import Button from '@/components/layout/Button';
import { getCachedClients } from '@/lib/mocked-fake'

const Page = () =>
{
    const router = useRouter();

    const [ data, setData ] = useState( true );
    const [ isLoading, setLoading ] = useState( true );

    useEffect( () =>
    {
        const clientArray = getCachedClients();
        setData( clientArray );
        setLoading( false );
    }, [] )

    if ( isLoading )
    {
        return <h1>Loading...</h1>;
    }

    if ( !data )
    {
        return <h1>No data found</h1>;
    }
    else
    {
        console.log(data)
    }

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
                    <SearchBar
                        clientArray={ data }
                        setClientArray={ setData }
                    />
                </div>
                <Banner title="Welcome" description="This is the page banner" />
                <BigCardList clientArray={ data } />
            </div>
            <OptionsSidebar>
                <Button
                    text="Add client"
                    type="primary"
                    width='90'
                    onClick={ () => router.push( '/clients/score/report/12345678000195' ) }
                />
                <Button
                    text="Risk clients"
                    type="secondary"
                    width='90'
                    onClick={ () => router.push( '/clients/score/report/12345678000195' ) }
                />
            </OptionsSidebar>
        </div>
    );
};

export default Page;
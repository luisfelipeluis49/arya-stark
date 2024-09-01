'use client'

import React, { useState } from 'react';
import MenuSidebar from '@/components/layout/MenuSidebar';
import OptionsSidebar from '@/components/layout/OptionsSidebar';
import Title from '@/components/layout/Title';
import Banner from '@/components/layout/Banner';
import FAB from '@/components/layout/FAButton';
import Input from '@/components/common/Input';
import Button from '@/components/common/Button';
import { useRouter } from 'next/navigation';

const Page = () =>
{
    const router = useRouter();

    const [ cnpj, setCNPJ ] = useState( '' );
    const handleSendCNPJ = async ( cnpj ) =>
    {
        try
        {
            const response =
                await fetch( 'http://localhost:8000/api/analyze',
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
                        pahtname: `http://localhost:8000/clients/report/${ data.slug }`,
                        query: { data: data }
                    }
                );
            };
        }
        catch ( error )
        {
            console.error( error );
        }
        setCNPJ( '' );
    };

    return (
        <div
            style=
            {
                {
                    display: 'flex',
                    flexDirection: 'row',
                    height: '100%',
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
                        flexDirection: 'column',
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
                <Input label="Enter your input" value={ cnpj } />
                <Button
                    text="Submit"
                    type="primary"
                    width="100%"
                    onClick={ handleSendCNPJ }
                />
            </div>
            <OptionsSidebar>
            </OptionsSidebar>
        </div>
    );
};

export default Page;

import React from 'react';
import TextField from '../layout/TextField';
import Dialog from '../layout/Dialog';

const TextDialog = ( { item } ) =>
{
    return (
        <Dialog>
            <div style={{ display: 'flex', flexDirection: 'row', fontSize: '24px', gap: '10px' }}>
                <div style={{ width: '70%', padding: '10px' }}>
                    <h2 style={{ color: '#000000' }}>{ item.title }</h2>
                    <TextField value={ item.description } />
                </div>
                <div style={{ width: '30%', padding: '10px' }}>
                    <ul>
                        {
                            item.references.map(
                                ( reference, index ) =>
                                (
                                    <li key={ index }>
                                        <a href={ reference.url } target='_blank'>
                                            { reference.title }
                                        </a>
                                    </li>
                                )
                            )
                        }
                    </ul>
                </div>
            </div>
        </Dialog>
    );
};

export default TextDialog;
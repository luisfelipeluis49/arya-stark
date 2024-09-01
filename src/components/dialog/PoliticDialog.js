import React from 'react';
import Input from '@/components/layout/Input';
import Button from '@/components/layout/Button';
import Dialog from '../layout/Dialog';

function PoliticDialog() {
    return (
        <Dialog>
            <div style={{ display: 'flex', flexDirection: 'row', fontSize: '24px', gap: '10px' }}>
                <div style={{ width: '70%', padding: '10px' }}>
                    <h2 style={{ color: '#000000' }}>Title</h2>
                    <Input label="Single Line Input" value="" />
                    <Input label="Multiline Input" value="" />
                </div>
                <div style={{ width: '30%', padding: '10px' }}>
                    <Button text="Primary" type="primary" width="90px" onClick={() => {}} />
                    <Button text="Secondary" type="secondary" width="90px" onClick={() => {}} />
                </div>
            </div>
        </Dialog>
    );
}

export default PoliticDialog;
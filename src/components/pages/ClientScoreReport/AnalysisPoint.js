import React from 'react';
import StatusBullet from '@/components/layout/StatusBullet';
import TextField from '@/components/layout/TextField';

const AnalysisPoint = ({ analysisPoint }) =>
{
    if ( analysisPoint.probability > 4.5)
    {
        analysisPoint.color = 'red';
    }
    else if ( analysisPoint.probability > 2.5)
    {
        analysisPoint.color = 'orange';
    }
    else
    {
        analysisPoint.color = 'blue';
    }

    return (
        <div>
            <div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <div style={{ display: 'flex', alignItems: 'center' }}>
                        <StatusBullet color={ analysisPoint.color } />
                        <h4>{ analysisPoint.qualification }</h4>
                    </div>
                    <div style={{ display: 'flex', alignSelf: 'flex-end' }}>
                        <h4>{ analysisPoint.probability }</h4>
                    </div>
                </div>
                <div>
                        <TextField
                            label="Enter your analysis"
                            variant="outlined"
                            multiline
                            rows={ 4 }
                        />
                </div>
            </div>
        </div>
    );
};

export default AnalysisPoint;
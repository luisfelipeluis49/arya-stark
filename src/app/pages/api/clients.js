import { getCachedClients } from '@/lib/mocked-fake'

export default function handler( req, res )
{
    const clientArray = getCachedClients();

    return res.status( 200 ).json( { clientArray } )
}
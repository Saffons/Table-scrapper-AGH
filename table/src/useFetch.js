import {useState, useEffect} from 'react';


const useFetch = (endpoint) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);


    useEffect(() => {
        const abortCon = new AbortController();

        fetch(endpoint, {signal: abortCon.signal})
            .then(res => {
                if (!res.ok) {
                    throw Error('could not fetch data.')
                }
                return res.json();
            })
            .then(data => {
                setData(data);
                setLoading(false);
                setError(null);
            }).catch(err => {
                if (err.name === 'AbortError') {
                    console.log("fetch aborted");
                } 
                setLoading(false);
                setError(err.message);
            });

            return () => abortCon.abort();
    }, [endpoint]);

    return {data, loading, error};
}

export default useFetch;
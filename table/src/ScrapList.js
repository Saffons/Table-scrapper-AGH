import List from "./List";
import useFetch from "./useFetch";

const ScrapList = (props) => {
    const { data: scraps, loading, error } = useFetch("http://localhost:8000/scrap");
    return (
        <div className="scrap-list">
            {error && <div>{error}</div>}
            {loading && <div>Loading scraps...</div>}
            {scraps && <List scraps={scraps} />}
        </div>
    );
}

export default ScrapList;
import ScrapList from './ScrapList';
import useFetch from './useFetch';

const Home = () => {
    
    return (
        <div className="home">
            <h1>Homepage</h1>
            <p style={{
                margin: "20px 0px"
            }}>Welcome to Table Scrapper,
                a program that takes a screenshot of your numeric data table
                and returns its' values in a CSV file.
            </p>
            
        </div>

    );
}

export default Home;
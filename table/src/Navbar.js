import { Link } from 'react-router-dom';

const Navbar = () => {
    return (
        <nav className="navbar">
            <h1>Table Scrapper</h1>
            <div className="links">
                <Link to="/">Home</Link>
                <Link to="/scrap">Scrap a table</Link>
                <Link to="/tables">Your tables</Link>
                <Link to="/authors">Authors</Link>
            </div>
        </nav>
    );
}

export default Navbar;

import './App.css';
import Navbar from './Navbar';
import Home from './Home';
import Footer from './Footer';
import Scrap from './Scrap';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import ScrapList from './ScrapList';
import React from 'react';

function App() {
  return (
    <Router>
    <div className="App">
      <Navbar />
       <div className="content">
          <Switch>
            <Route exact path="/"> 
              <Home />
            </Route>
            <Route exact path="/scrap">
              <Scrap />  
            </Route>
            <Route exact path="/tables">
              <ScrapList />
            </Route> 
            <Route exact path="/authors">
              <Footer />
            </Route>
          </Switch>
       </div>
    </div>
    </Router>
  );
}

export default App;

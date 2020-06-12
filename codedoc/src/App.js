import React from 'react';
import logo from './logo.svg';
import 'carbon-components/css/carbon-components.min.css'
import { Welcome, Calendar } from './screens'
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { NavigationBar } from './components/NavigationBar';

function App() {
  return (
    <React.Fragment>
      <Router>
        <NavigationBar />
        <div className="App">
          <Welcome />
          <Calendar />
        </div>
      </Router>
    </React.Fragment>
    
  );
}

export default App;

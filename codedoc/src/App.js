import React from 'react';
import logo from './logo.svg';
import 'carbon-components/css/carbon-components.min.css'
import { Welcome } from './screens'
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
          <Switch>
            <Route exact path="/">
              <WelcomePage />
            </Route>
            <Route path="/profile">
              <Profile />
            </Route>
            <Route path="/calendar">
              <Calendar />
            </Route>
        </Switch>
        </div>
      </Router>
    </React.Fragment>
    
  );
}

function WelcomePage() {
    return (
        <Welcome />
    );
}

// function Profile() {
//     return (
//         <Profile />
//     );
// }
  
function Calendar() {
    return (
        <Calendar />
    );
}

export default App;

import React from 'react';
import logo from './logo.svg';
import 'carbon-components/css/carbon-components.min.css'
import { Welcome, Calendar, Profile } from './screens'
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { NavigationBar } from './components/NavigationBar';

function App() {
  return (
    <React.Fragment>
      <Router>
        <NavigationBar />
        <div className="App">
          <Switch>
            <Route exact path="/">
              <WelcomePage />
            </Route>
            <Route path="/profile">
              <ProfilePage />
            </Route> 
            <Route path="/calendar">
              <CalendarPage />
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

function ProfilePage() {
    return (
        <Profile />
    );
}
  
function CalendarPage() {
    return (
        <Calendar />
    );
}

export default App;

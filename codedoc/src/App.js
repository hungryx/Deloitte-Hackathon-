import React from 'react';
import logo from './logo.svg';
import 'carbon-components/css/carbon-components.min.css'
import { Welcome, Calendar } from './screens'

function App() {
  return (
    <div className="App">
      <Welcome />
      <Calendar />
    </div>
  );
}

export default App;

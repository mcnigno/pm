import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from 'react';
import Avatar from './components/user_components'
import Timesheet from './components/timesheet'
import Billable from './components/billable'
import BootstrapTable from 'react-bootstrap-table-next'

 
function App() {
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/timesheetview/api/read').then(res => res.json()).then(data => {
      setCurrentTime(data.result[0]['id']);
    })
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <p>The current time is {currentTime.toString()}.</p>
        <Avatar bname='' name="Vandro"></Avatar>
        
        <Billable></Billable>
      </header>
    </div>
  );
}

export default App;

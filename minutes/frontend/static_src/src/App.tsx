import React from 'react';
import {BrowserRouter as Router, Switch} from 'react-router-dom';
import {RouterOutlet} from "./components/RouterOutlet";
import {useRoutes} from "./routes";

function App() {
  const routeConfig = useRoutes()
  return (
    <Router>
      <Switch>
        <RouterOutlet routes={routeConfig.routes}/>
      </Switch>
    </Router>
  )
}

export default App;

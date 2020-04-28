import React from 'react';
import {BrowserRouter as Router, Link, Route, Switch} from 'react-router-dom';
import {Alignment, Button, Navbar} from "@blueprintjs/core";
import MeetingSeries from "./MeetingSeries";
import Administration from "./Administration";

class App extends React.Component {
  render(): React.ReactNode {
    return (
      <Router>
        <Navbar>
          <Navbar.Group align={Alignment.LEFT}>
            <Navbar.Heading>Minutes</Navbar.Heading>
            <Navbar.Divider/>
            <Link to="/series">
              <Button className="bp3-minimal" icon="pulse" text="Meeting Series"/>
            </Link>
            <Link to="/administration">
              <Button className="bp3-minimal" icon="settings" text="Administration"/>
            </Link>
          </Navbar.Group>
        </Navbar>
        <Switch>
          <Route path="/series">
            <MeetingSeries />
          </Route>
          <Route path="/administration">
            <Administration />
          </Route>
        </Switch>
      </Router>
    );
  }
}

export default App;

import React, {useEffect} from 'react';
import {BrowserRouter as Router, Link, Switch, useHistory, Redirect} from 'react-router-dom';
import {Alignment, Button, Menu, MenuItem, Navbar, Popover, Position} from "@blueprintjs/core";
import {RouterOutlet} from "../components/RouterOutlet";
import {Breadcrumbs} from "../components/Breadcrumbs";
import styles from './MemberArea.module.scss'
import {RouteId, useRoutes} from "../routes";
import {IRoutedComponentProps} from "../components/RoutedComponent";
import {MINIMAL} from "@blueprintjs/core/lib/esm/common/classes";
import {useStores} from "../store";
import {createApiClient} from "../api/client";
import {observer} from "mobx-react";


function MemberArea({routes}: IRoutedComponentProps) {
  const routeConfig = useRoutes()
  const stores = useStores()
  const history = useHistory()

  useEffect(() => {
    const minutesApi = createApiClient().minutesApi
    minutesApi.retrieveUser({id: 'me'}).then((user) => stores.user.setCurrentUser(user))

  }, [stores.user])

  const loginPath = routeConfig.idToRoute(RouteId.LOGIN).path
  const logout = () => {
    stores.credentials.setTokenSet(null)
    history.push(loginPath)
  }
  if (!stores.credentials.hasValidToken) {
    return (<Redirect to={routeConfig.idToRoute(RouteId.LOGIN).path}/>)
  }

  return (
      <Router>
        <Navbar className={`container`}>
          <Navbar.Group align={Alignment.LEFT}>
            <Navbar.Heading>Minutes</Navbar.Heading>
            <Navbar.Divider/>
            <Link to={routeConfig.idToRoute(RouteId.MEETING_SERIES)!!.path}>
              <Button className={MINIMAL} icon="pulse" text="Meeting Series"/>
            </Link>
            <Link to={routeConfig.idToRoute(RouteId.ADMIN)!!.path}>
              <Button className={MINIMAL} icon="settings" text="Administration"/>
            </Link>
            <Navbar.Divider/>
            <Navbar.Heading>{stores.user.currentUser?.username}</Navbar.Heading>
            <Popover content={
              <Menu>
                <MenuItem onClick={logout} icon="log-out" text="Logout"/>
              </Menu>
            } position={Position.BOTTOM_RIGHT}>
              <Button icon="user" className={MINIMAL}/>
            </Popover>
          </Navbar.Group>
        </Navbar>
        <React.Fragment>

          <div className={`container ${styles.BreadcrumbsContainer}`}>
            <Breadcrumbs/>
          </div>
          <div className={`container ${styles.BreadcrumbsContainer}`}>
            <Switch>
              <RouterOutlet routes={routes}/>
            </Switch>
          </div>
        </React.Fragment>
      </Router>
  );
}

export default observer(MemberArea);

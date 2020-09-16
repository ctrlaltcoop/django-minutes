import React from 'react';
import {Menu, MenuItem} from "@blueprintjs/core";
import {RouterOutlet} from "../components/RouterOutlet";
import {Link, Switch} from "react-router-dom"
import {idToRoute, RouteId} from "../routes";
import {IRoutedComponentProps} from "../components/RoutedComponent";

function Administration({ routes }: IRoutedComponentProps) {
  return (
    <div className="container main h-100">
      <div className="row h-100">
        <div className={`sidebar col-2 h-100`}>
          <Menu>
            <Link to={idToRoute(RouteId.ADMIN_USERS)!!.path}>
                <MenuItem tagName="span" text="Users" icon="user" />
            </Link>
          </Menu>
        </div>
        <div className={`content-area col-10`}>
          <Switch>
            <RouterOutlet routes={routes}/>
          </Switch>
        </div>
      </div>
    </div>
  )
}

export default Administration;

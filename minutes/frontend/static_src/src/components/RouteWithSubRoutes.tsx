import React from "react";
import {Route} from 'react-router-dom';
import {RouteConfig} from "../routes";

export interface IRouteWithSubRoutesProps {
  route: RouteConfig
}

export function RouteWithSubRoutes(props: IRouteWithSubRoutesProps) {
  const route = props.route
  const Component = route.component
  return (
    <Route
      path={route.path}
      exact={route.exact ?? false}
      render={props => (
        // pass the sub-routes down to keep nesting
        <Component routes={route.routes}/>
      )}
    />
  );
}


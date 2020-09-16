import React from "react";
import {RouteWithSubRoutes} from "./RouteWithSubRoutes";
import {IRoutedComponentProps} from "./RoutedComponent";


export function RouterOutlet(props: IRoutedComponentProps)  {
  return (
    <React.Fragment>{props.routes?.map((route, i) => (
      <RouteWithSubRoutes key={i} route={route} />
    ))}
    </React.Fragment>
  )
}

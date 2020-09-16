import MeetingSeriesList from "./views/MeetingSeriesList";
import Administration from "./views/Administration";
import Users from "./views/administration/Users";
import React, {LazyExoticComponent} from "react";

import {Redirect} from "react-router-dom"
import {IRoutedComponentProps} from "./components/RoutedComponent";
import Login from "./views/Login";
import MemberArea from "./views/MemberArea";
import UserDetail from "./views/administration/UserDetail";

type RoutableComponent =
  (({routes}: IRoutedComponentProps) => JSX.Element) |
  React.ComponentClass<IRoutedComponentProps> |
  LazyExoticComponent<any>

export type RouteConfig = {
  id?: RouteId,
  path: string,
  exact?: boolean,
  component: RoutableComponent,
  routes?: Array<RouteConfig>,
  breadcrumb?: string,
}

export enum RouteId {
  HOME,
  LOGIN,
  MEMBER_AREA,
  MEETING_SERIES,
  ADMIN,
  ADMIN_USERS,
  ADMIN_USER_DETAIL
}

export function idToRoute(findId: RouteId, params: { [name: string]: string } = {}, searchRoutes: Array<RouteConfig> = routes): RouteConfig {
  const paramRegex = /:[\w]+/
  for (let route of searchRoutes) {
    if (route.id === findId) {
      return {
        ...route,
        // @ts-ignore
        path: route.path.replace(paramRegex, (match) => params[match.slice(1)])
      }
    } else if (route.routes !== undefined) {
      return idToRoute(findId, params, route.routes)
    }
  }
  throw Error(`Route id ${findId} not found in tree`)
}

/**
 * Route matching in react router always works via absolute paths /u/some/page
 * While declaring a nested route hierarchy that's inconvenient, so we decrlare routes
 * in hierarchy with only the relevant segment and have this helper function to transform them
 * all to absolutes
 */
export function expandPaths(routes: Array<RouteConfig>, parentPath = ''): Array<RouteConfig> {
  return routes.map((route) => {
    const thisPath = parentPath + route.path
    return {
      ...route,
      path: thisPath,
      routes: route.routes ? expandPaths(route.routes, thisPath) : undefined
    }
  })
}

const routeConfigs: Array<RouteConfig> = [
  {
    id: RouteId.HOME,
    path: "/",
    exact: true,
    component: () => <Redirect to="/login"/>,
  },
  {
    id: RouteId.LOGIN,
    path: "/login",
    exact: true,
    component: Login,
  },
  {
    id: RouteId.MEMBER_AREA,
    path: "/u",
    component: MemberArea,
    routes: [
      {
        path: "",
        exact: true,
        component: () => <Redirect to={idToRoute(RouteId.MEETING_SERIES)!!.path}/>
      },
      {
        id: RouteId.MEETING_SERIES,
        path: "/meeting-series",
        component: MeetingSeriesList,
        breadcrumb: "Meeting Series"
      },
      {
        id: RouteId.ADMIN,
        path: "/administration",
        component: Administration,
        breadcrumb: "Administration",
        routes: [
          {
            id: RouteId.ADMIN,
            path: "",
            exact: true,
            component: () => <Redirect to={idToRoute(RouteId.ADMIN_USERS)!!.path}/>
          },
          {
            id: RouteId.ADMIN_USERS,
            exact: true,
            path: "/users",
            component: Users,
            breadcrumb: "Users",
          },
          {
            id: RouteId.ADMIN_USER_DETAIL,
            path: "/users/:id",
            component: UserDetail,
            breadcrumb: "User",
          }
        ]
      }
    ]
  },
];

const routes = expandPaths(routeConfigs)
const RoutesContext = React.createContext({
  routes,
  idToRoute
})

export const useRoutes = () => React.useContext(RoutesContext)

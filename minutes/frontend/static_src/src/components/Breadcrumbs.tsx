import React from "react";
import {Breadcrumb, Breadcrumbs as BlueprintJSBreadcrumbs, IBreadcrumbProps, Icon} from "@blueprintjs/core";
import {Link} from "react-router-dom"
import useBreadcrumbs from "use-react-router-breadcrumbs";
import {IRoutedComponentProps} from "./RoutedComponent";
import {useRoutes} from "../routes";

export function Breadcrumbs(props: IRoutedComponentProps) {
  const routeConfig = useRoutes()
  const breadcrumbs = useBreadcrumbs(routeConfig.routes, { disableDefaults: true })
  const breadcrumbRenderer = ({text, href, icon, ...restProps}: IBreadcrumbProps): JSX.Element => {
    return (
      <Breadcrumb {...restProps}>
        <Icon icon={icon} />
        <Link to={href as string}>{text}</Link>
      </Breadcrumb>
    )
  }

  const breadcrumbItems = breadcrumbs.map(({breadcrumb, match}) => {
    return {
      href: match.url,
      text: breadcrumb
    }
  })
  return (
    <BlueprintJSBreadcrumbs items={breadcrumbItems} breadcrumbRenderer={breadcrumbRenderer}/>
  )

}
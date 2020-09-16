import React, {ReactNode} from "react";
import {Button, NonIdealState, Spinner} from "@blueprintjs/core";
import {ResourceState} from "../types/ResourceState";

interface IResourceStateManagerProps {
  state: ResourceState,
  children: ReactNode,
  onTryAgain: (...args: any) => any
}

export function ResourceStateManager(props: IResourceStateManagerProps) {

  return (
      <div className="resource-manager">
        {props.state === ResourceState.Failed &&
        <NonIdealState
            icon="warning-sign"
            title="Failed loading resource"
            action={<Button text="Try again" onClick={() => props.onTryAgain()} />} />
        }
        {props.state === ResourceState.Loaded && props.children}
        {props.state === ResourceState.Loading &&
            <Spinner size={100} />
        }
      </div>
  )

}
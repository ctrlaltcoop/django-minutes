import React, {useEffect, useState} from 'react';
import {ResourceStateManager} from "../components/ResourceStateManager";
import {ResourceState} from "../types/ResourceState";
import {MeetingSeries} from "../api/models";
import {Card, Icon, Intent} from "@blueprintjs/core";
import {createApiClient} from "../api/client";

const minutesApi = createApiClient().minutesApi

function MeetingSeriesList() {
  const [meetingSeries, setMeetingSeries] = useState<Array<MeetingSeries>>([])
  const [resourceState, setResourceState] = useState<ResourceState>(ResourceState.Initial)
  const getMeetingSeries = async () => {
    try {
      setResourceState(ResourceState.Loading)
      const series = await minutesApi.listMeetingSeries({})
      setResourceState(ResourceState.Loaded)
      setMeetingSeries(series?.results ?? [])
    } catch (e) {
      setResourceState(ResourceState.Failed)
    }
  }

  useEffect(() => {
    getMeetingSeries()
  }, [])

  return (
      <ResourceStateManager state={resourceState} onTryAgain={getMeetingSeries}>
        {meetingSeries.map((item) => {
          return (
              <Card key={item.id} className='d-flex flex-row' interactive={true}>
                <div>
                  <h5><a href="#">{item.name}</a></h5>
                  <p>{item.description}</p>
                </div>
                <div>
                  <Icon icon='caret-right' intent={Intent.PRIMARY}/>
                </div>
              </Card>
          )
        })}

      </ResourceStateManager>
  )
}

export default MeetingSeriesList;

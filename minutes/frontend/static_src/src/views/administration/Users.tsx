import React, {useEffect, useState} from 'react';
import {User} from "../../api";
import {Card, Icon} from "@blueprintjs/core";
import {Link} from "react-router-dom"
import {idToRoute, RouteId} from "../../routes";
import {ResourceStateManager} from "../../components/ResourceStateManager";
import {ResourceState} from "../../types/ResourceState";
import {createApiClient} from "../../api/client";
import useStateIfMounted from "../../utils/useStateIfMounted";

function Users() {
  const [retry, setRetry] = useState<number>(0)
  const [resourceState, setResourceState] = useStateIfMounted<ResourceState>(ResourceState.Initial)
  const [users, setUsers] = useStateIfMounted<User[]>([])


  useEffect(() => {
    const getUsers = async () => {
      const minutesApi = createApiClient().minutesApi
      setResourceState(ResourceState.Loading)
      try {
        const usersResponse = await minutesApi.listUsers({limit: 25, offset: 0})
        setUsers(usersResponse.results ?? [])
        setResourceState(ResourceState.Loaded)
      } catch (e) {
        setResourceState(ResourceState.Failed)
      }
    }
    getUsers()
    //eslint-disable-next-line react-hooks/exhaustive-deps
  }, [retry]);

  return (
      <ResourceStateManager state={resourceState} onTryAgain={() => setRetry(retry + 1)}>
        <Card>
          <table className="bp3-html-table">
            <thead>
            <tr>
              <th>Id</th>
              <th>Username</th>
              <th>First name</th>
              <th>Last name</th>
              <th>E-Mail</th>
              <th>Last login</th>
              <th>Actions</th>
            </tr>
            </thead>
            <tbody>
            {users.map((user) =>
                <tr key={user.id}>
                  <td>{user.id}</td>
                  <td>{user.username}</td>
                  <td>{user.firstName}</td>
                  <td>{user.lastName}</td>
                  <td>{user.email}</td>
                  <td>{user.lastLogin?.toLocaleString()}</td>
                  <td>
                    <Link to={idToRoute(RouteId.ADMIN_USER_DETAIL, {id: user.id!!.toString()}).path}>
                      <Icon icon={"edit"}/>
                    </Link>
                  </td>
                </tr>
            )}
            </tbody>
          </table>
        </Card>
      </ResourceStateManager>
  )
}

export default Users;

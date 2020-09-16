import React, {useEffect, useState} from 'react';
import {User} from "../../api";
import {createApiClient} from "../../api/client";
import {Alert, Button, ButtonGroup, Card, Checkbox, FormGroup, InputGroup, Toaster} from "@blueprintjs/core";
import {useHistory, useParams} from "react-router-dom"
import {Intent} from "@blueprintjs/core/lib/esm/common/intent";
import {ResourceStateManager} from "../../components/ResourceStateManager";
import {ResourceState} from "../../types/ResourceState";
import {idToRoute, RouteId} from "../../routes";

const toaster = Toaster.create()
const minutesApi = createApiClient().minutesApi

function UserDetail() {
  const [retry, setRetry] = useState();

  const params = useParams<any>()
  const history = useHistory()

  const [resourceState, setResourceState] = useState<ResourceState>(ResourceState.Initial)
  const [saveState, setSaveState] = useState<ResourceState>(ResourceState.Initial)
  const [deleteState, setDeleteState] = useState<ResourceState>(ResourceState.Initial)
  const [errors, setErrors] = useState<{ [key: string]: string }>()
  const [user, setUser] = useState<Partial<User> | null>(null)
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState<boolean>(false)


  const handleUserFormInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setUser({
      ...user,
      [event.target.name]: event.target.value
    })
  }

  const handleUserFormCheckboxChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setUser({
      ...user,
      [event.target.name]: event.target.checked
    })
  }

  useEffect(() => {
    const getUser = async () => {
      try {
        setResourceState(ResourceState.Loading)
        const usersResponse = await minutesApi.retrieveUser({id: params.id})
        setUser(usersResponse ?? null)
        setResourceState(ResourceState.Loaded)
      } catch (e) {
        setResourceState(ResourceState.Failed)
        setUser(null)
      }
    }
    getUser()
  }, [params, retry]);

  const saveUser = async () => {
    setErrors({})
    setSaveState(ResourceState.Loading)
    try {
      if (user?.id === undefined) {
        await minutesApi.createUser({user: user as User})
      } else {
        await minutesApi.updateUser({id: user.id.toString(), user: user as User})
      }
      setSaveState(ResourceState.Loaded)
      toaster.show({intent: Intent.SUCCESS, message: 'User saved'})
    } catch (e) {
      setSaveState(ResourceState.Failed)
      if (e.status === 400) {
        setErrors(await e.json())
      } else {
        toaster.show({intent: Intent.DANGER, message: 'Unknown error while saving user'})
      }
    }
  }

  const deleteUser = async () => {
    setDeleteConfirmOpen(false)
    if (user?.id !== undefined) {
      setDeleteState(ResourceState.Loading)
      try {
        await minutesApi.destroyUser({id: user.id.toString()})
        toaster.show({
          intent: Intent.SUCCESS,
          message: 'User deleted'
        })
        setDeleteState(ResourceState.Loaded)
        history.push(idToRoute(RouteId.ADMIN_USERS).path)
      } catch (e) {
        setResourceState(ResourceState.Failed)
        toaster.show({
          intent: Intent.DANGER,
          message: 'Failed to delete user'
        })
      }
    }
  }

  const FormError = (props: { message: undefined | string }) => {
    if (props.message) {
      return (
          <span className='error-message'>{props.message}</span>
      )
    } else {
      return null
    }
  }

  return (
      <Card>
        <ResourceStateManager state={resourceState} onTryAgain={setRetry}>
          <form>
            <FormGroup
                label="Username"
                labelFor="username"
            >
              <InputGroup
                  readOnly={true}
                  intent={errors?.email ? Intent.DANGER : Intent.NONE}
                  value={user?.username}
                  id="username" placeholder="username" name="username"
                  onChange={handleUserFormInputChange}/>
            </FormGroup>
            <FormError message={errors?.username}/>
            <FormGroup
                label="First name"
                labelFor="firstName"
            >
              <InputGroup value={user?.firstName}
                          id="firstName" placeholder="First name" name="firstName"
                          onChange={handleUserFormInputChange}/>
            </FormGroup>
            <FormError message={errors?.firstName}/>
            <FormGroup
                label="Last name"
                labelFor="lastName"
            >
              <InputGroup
                  intent={errors?.email ? Intent.DANGER : Intent.NONE}
                  value={user?.lastName}
                  id="lastName"
                  placeholder="Last name"
                  name="lastName"
                  onChange={handleUserFormInputChange}/>
            </FormGroup>
            <FormError message={errors?.lastName}/>
            <FormGroup
                label="E-Mail"
                labelFor="email"
            >
              <InputGroup
                  intent={errors?.email ? Intent.DANGER : Intent.NONE}
                  value={user?.email}
                  id="email"
                  placeholder="email address"
                  name="email"
                  onChange={handleUserFormInputChange}/>
              <FormError message={errors?.email}/>
            </FormGroup>
            <FormGroup
                label="Administrator"
                labelFor="isSuperuser"
            >
              <Checkbox
                  checked={user?.isSuperuser}
                  id="isSuperuser"
                  name="isSuperuser"
                  onChange={handleUserFormCheckboxChange}/>
            </FormGroup>
            <ButtonGroup>
              <Button loading={saveState === ResourceState.Loading} intent={Intent.PRIMARY} icon="floppy-disk"
                      onClick={saveUser}>Save</Button>
              <Button loading={deleteState === ResourceState.Loading} intent={Intent.DANGER} icon="trash"
                      onClick={() => setDeleteConfirmOpen(true)}>Delete</Button>
            </ButtonGroup>

          </form>
        </ResourceStateManager>
        <Alert intent={Intent.DANGER}
               icon="trash"
               cancelButtonText="Cancel"
               confirmButtonText="Delete"
               onConfirm={deleteUser}
               isOpen={deleteConfirmOpen}
               onCancel={() => setDeleteConfirmOpen(false)}
        >Are you sure you want to delete user <b>{user?.username}</b>?</Alert>
      </Card>

  )
}

export default UserDetail;

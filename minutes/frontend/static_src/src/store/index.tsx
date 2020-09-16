import { SyncTrunk } from 'mobx-sync/lib/sync';
import CredentialsStore from './CredentialsStore';
import React from "react";
import UserStore from "./UserStore";

export const credentialsStore = new CredentialsStore()

const trunk = new SyncTrunk(credentialsStore, { storage: localStorage });
trunk.init()

const StoresContext = React.createContext({
  credentials: credentialsStore,
  user: new UserStore()
})

export const useStores = () => React.useContext(StoresContext)

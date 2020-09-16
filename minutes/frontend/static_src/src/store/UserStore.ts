import {action, observable} from "mobx";
import {User} from "../api/models";

export default class UserStore {
  @observable
  currentUser: User | null = null

  @action
  setCurrentUser(user: User) {
    this.currentUser = user
  }
}
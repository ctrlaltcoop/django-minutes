import {action, computed, observable} from "mobx";
import {TokenSet} from "../api/models/TokenSet";
import {date} from "mobx-sync";

export default class CredentialsStore {
  @observable
  authToken: string | null = null

  @observable
  @date
  authTokenExpires: Date | null = null

  @observable
  refreshToken: string | null = null
  @observable
  @date
  refreshTokenExpires: Date | null = null

  @action
  setTokenSet(tokenSet: TokenSet | null) {
    if (tokenSet === null) {
      this.authToken = this.authTokenExpires = this.refreshToken = this.refreshTokenExpires = null
    } else {
      this.authToken = tokenSet.authTokenKey
      this.authTokenExpires = tokenSet.authTokenExpires
      this.refreshToken = tokenSet.refreshTokenKey
      this.refreshTokenExpires = tokenSet.refreshTokenExpires
    }
  }

  @computed
  get hasValidToken(): boolean {
    return this.authToken !== null && (this.authTokenExpires ?? new Date()) > new Date()
  }
}
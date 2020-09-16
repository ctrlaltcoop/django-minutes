import {AuthApi, MinutesApi} from "./apis";
import {Configuration, FetchParams, Middleware, RequestContext, ResponseContext} from "./runtime";
import {credentialsStore} from "../store";
import {TokenSet} from "./models/TokenSet";


const apiConfiguration = {
  basePath: process.env.REACT_APP_API_BASE_PATH
}

function addBearerTokenToInit(init: RequestInit, authToken: string): RequestInit {
  return {
    ...init,
    headers: {
      ...init.headers,
      Authorization: `Token ${authToken}`
    }
  }
}

class AuthenticationMiddleware implements Middleware {

  /**
   *
   * @param url
   * @param init
   * @return FetchParams fetch aparams containing authentication credentials if present
   */
  async pre({url, init}: RequestContext): Promise<FetchParams | void> {
    if (credentialsStore.authToken !== null) {
      return {
        url,
        init: addBearerTokenToInit(init, credentialsStore.authToken!!)
      }
    } else {
      return {url, init}
    }
  }

  async post(context: ResponseContext): Promise<Response | void> {
    if (
      context.response.status === 401
      && credentialsStore.refreshToken !== null
      && (credentialsStore.refreshTokenExpires ?? new Date()) > new Date()
    ) {
      try {
        const authApi = createApiClient().authApi

        const refreshResponse = await authApi.createTokenSetByRefresh({
          tokenRefresh: {
            refreshToken: credentialsStore.refreshToken,
          }
        }) as TokenSet
        credentialsStore.setTokenSet(refreshResponse)
        return context.fetch(context.url, addBearerTokenToInit(context.init, refreshResponse.authTokenKey))
      } catch (e) {
        debugger
        // If we can't recover from 401 logout
        credentialsStore.setTokenSet(null)
      }
    }
    // if didn't return before just pass original response
    return context.response
  }
}


export function createApiClient(abortController: AbortController | null = null) {


  const abortableFetch = (url: string, params: RequestInit | undefined): Promise<Response> => {
    params = params || {}
    params.signal = abortController?.signal
    return fetch(url, params)
  }
  const config = new Configuration({
    ...apiConfiguration,
    fetchApi: abortableFetch
  })
  const minutesApi = new MinutesApi(config)
      .withMiddleware(new AuthenticationMiddleware())
  const authApi = new AuthApi(config)

  return {
    minutesApi,
    authApi
  }
}
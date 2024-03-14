import fetch, { Headers, HeadersInit, RequestInit as FetchRequestInit } from 'node-fetch'
import { RestAPI, RestAPIMeta } from './types'

export interface Response<Body> {
    body: Body
    meta: {
        headers: Headers
        status: number
    }
}

export interface ClientOptions {
    baseUrl?: string
    credentials?: {
        clientId: string
        clientSecret: string
    }
}

/**
 * Get the timestamp as the number of seconds from the UNIX epoch.
 * @returns the UNIX timestamp with a resolution of one second
 */
const currTimestamp = (): number => Math.floor(Date.now() / 1e3)
export const expiryThreshold = 5 // seconds

type RequestInit<T extends keyof RestAPI> = {
    headers?: HeadersInit
} & (RestAPI[T]["params"] extends null ? {} : { params: RestAPI[T]["params"] })

export const OpenverseClient = ({ baseUrl = "https://api.openverse.engineering/", credentials }: ClientOptions = {}) => {

    let apiToken: RestAPI['POST v1/auth_tokens/token/']["response"] | null = null
    let tokenExpiry: number | null = null

    const normalisedBaseUrl = baseUrl.endsWith('/') ? baseUrl : `${baseUrl}/`

    const baseRequest = async <T extends keyof RestAPI>(endpoint: T, { headers, ...req }: RequestInit<T>): Promise<Response<RestAPI[T]["response"]>> => {
        let [method, url] = endpoint.split(" ")
        const endpointMeta = RestAPIMeta[endpoint]

        const params = "params" in req ? {...req.params as Record<string, any>} : {}
        endpointMeta.pathParams.forEach((param) => {
            url = url.replace(`:${param}`, params[param])
            delete params[param]
        })

        const finalHeaders = new Headers(headers)
        if (!finalHeaders.has("content-type")) {
            finalHeaders.set("content-type", endpointMeta.contentType)
        }

        const requestConfig: FetchRequestInit = {
            method,
            headers: finalHeaders,
        }

        if (method === "POST") {
            requestConfig["body"] = JSON.stringify(params)
        } else {
            const search = new URLSearchParams(params)
            url = `${url}?${search}`
        }

        const fullUrl = `${normalisedBaseUrl}${url}`
        console.error(fullUrl)
        const response = await fetch(fullUrl, requestConfig)

        const body = endpointMeta.jsonResponse ? await response.json() : response.body
        return {
            body: body as RestAPI[T]["response"],
            meta: {
                headers: response.headers,
                status: response.status,
            },
        }
    }

    const getAuthHeaders = async (headers: HeadersInit): Promise<Headers> => {
        if (!credentials) {
            return new Headers(headers)
        }

        if (!(apiToken && tokenExpiry) || tokenExpiry - expiryThreshold < currTimestamp()) {
            const tokenResponse = await baseRequest("POST v1/auth_tokens/token/", {
                params: {
                    grant_type: "client_credentials",
                    client_id: credentials.clientId,
                    client_secret: credentials.clientSecret,
                }
            })
            tokenExpiry = currTimestamp() + tokenResponse.body.expires_in
    
            apiToken = tokenResponse.body
        }

        const withAuth = new Headers(headers)

        withAuth.append('Authorization', `Bearer: ${apiToken.access_token}`)
        return withAuth
    }

    const request = async <T extends keyof RestAPI>(endpoint: T, req: RequestInit<T>): Promise<Response<RestAPI[T]["response"]>> => {
        const authHeaders = await getAuthHeaders(req.headers ?? {})
        return baseRequest(endpoint, { ...req, headers: authHeaders })
    }

    return request
}

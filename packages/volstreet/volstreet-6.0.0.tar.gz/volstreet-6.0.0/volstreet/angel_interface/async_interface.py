import aiohttp
import json
import asyncio
from datetime import datetime
from asyncio import Task
from SmartApi.smartConnect import SmartConnect, urljoin, logger


class AsyncSmartConnect(SmartConnect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def _async_request(
        self, route, method, parameters=None, appendage="", session=None
    ):
        if session is None:
            async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=self.ssl_context)
            ) as session:
                return await self._async_request(
                    route, method, parameters, appendage, session
                )

        if appendage:
            url = urljoin(self._rootUrl, self._routes[route] + appendage)
            params = {}
        else:
            params = parameters.copy() if parameters else {}
            uri = self._routes[route].format(**params)
            url = urljoin(self.root, uri)

        headers = self.requestHeaders()

        if self.access_token:
            auth_header = self.access_token
            headers["Authorization"] = f"Bearer {auth_header}"

        try:
            async with session.request(
                method,
                url,
                data=json.dumps(params) if method in ["POST", "PUT"] else None,
                params=json.dumps(params) if method in ["GET", "DELETE"] else None,
                headers=headers,
                verify_ssl=not self.disable_ssl,
                timeout=self.timeout,
            ) as response:
                try:
                    data = await response.json()
                    return data
                except Exception as e:
                    logger.error(
                        f"Error occurred while converting response. Response text: {await response.text()}, "
                    )
                    raise e

        except Exception as e:
            logger.error(
                f"Error occurred while making a {method} request to {url}. Headers: {headers}, Request: {params}, Response: {e}"
            )
            raise e

    async def async_delete_request(self, route, parameters=None, session=None):
        return await self._async_request(route, "DELETE", parameters, session)

    async def async_get_request(self, route, parameters=None, session=None):
        return await self._async_request(route, "GET", parameters, session)

    async def async_post_request(self, route, parameters=None, session=None):
        return await self._async_request(route, "POST", parameters, session)

    async def async_put_request(self, route, parameters=None, session=None):
        return await self._async_request(route, "PUT", parameters, session)

    async def async_login(self, user, password, totp, session=None):
        params = {"clientcode": user, "password": password, "totp": totp}
        login_result = await self.async_post_request("api.login", params, session)

        if login_result["status"] is True:
            self.setAccessToken(login_result["data"]["jwtToken"])
            self.setRefreshToken(login_result["data"]["refreshToken"])
            self.setFeedToken(login_result["data"]["feedToken"])
            user = self.getProfile(self.refresh_token)
            user_id = user["data"]["clientcode"]
            self.setUserId(user_id)
            user["data"]["jwtToken"] = "Bearer " + self.access_token
            user["data"]["refreshToken"] = self.refresh_token
            user["data"]["feedToken"] = self.feed_token
            return user
        else:
            return login_result

    async def async_get_ltp(self, params, session=None):
        response = await self.async_post_request("api.ltp.data", params, session)
        return response

    async def async_place_order(self, order_params, session=None):
        params = order_params
        for k in list(params.keys()):
            if params[k] is None:
                del params[k]
        response = await self.async_post_request("api.order.place", params, session)
        if response is not None and response.get("status", False):
            if (
                "data" in response
                and response["data"] is not None
                and "orderid" in response["data"]
            ):
                return response
            else:
                logger.error(f"Invalid response format: {response}")
        else:
            logger.error(f"API request failed: {response}")
        return None

    async def async_modify_order(self, modified_params, session=None):
        params = modified_params

        for k in list(params.keys()):
            if params[k] is None:
                del params[k]

        response = await self.async_post_request("api.order.modify", params, session)
        return response

    async def individual_order_status(self, unique_order_id, session=None):
        response = await self._async_request(
            "api.individual.order.details",
            "GET",
            appendage=unique_order_id,
            session=session,
        )
        return response


async def rate_handler(
    tasks: list[Task],
    requests_per_sec: int,
) -> None:
    """ A generator that yield results as and when they become available. Handles rate limiting."""
    pending = set()
    start_times = []

    def remove_expired_start_times():
        nonlocal start_times
        time_now = datetime.now()
        start_times = [t for t in start_times if (time_now - t).total_seconds() < 1.1]

    while tasks or pending:
        remove_expired_start_times()
        while len(start_times) < requests_per_sec:
            try:
                task = tasks.pop(0)
            except IndexError:
                break
            start_times.append(datetime.now())
            pending.add(asyncio.ensure_future(task))

        if not pending:
            if tasks:
                oldest_time = min(start_times)
                sleep_time = (oldest_time - datetime.now()).total_seconds()
                await asyncio.sleep(sleep_time)
                continue
            else:
                return

        done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

        while done:
            yield done.pop().result()

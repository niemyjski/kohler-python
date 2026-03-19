"""Kohler DTV+ device control library."""

from __future__ import annotations

import asyncio
import contextlib
import json
import logging
import secrets
import urllib.parse
from pathlib import Path
from typing import Any

_LOGGER = logging.getLogger(__name__)

CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_TEXT_PLAIN = "text/plain"
UPLOAD_CHUNK_SIZE = 64 * 1024


class KohlerError(Exception):
    """Raised when a Kohler device communication error occurs."""


class Kohler:
    """Asynchronous client for controlling Kohler DTV+ shower systems.

    Args:
        kohler_host: The IP address or hostname of the Kohler DTV+ device.
        timeout: Default connection and read timeout in seconds.
    """

    def __init__(self, kohler_host: str, timeout: float = 1.0) -> None:
        self._host = kohler_host
        self._base_url = f"http://{kohler_host}"
        self.timeout = timeout

    async def bt_disconnect(self) -> Any:
        url = f"{self._base_url}/bt_disconnect.cgi"
        return await self._fetch(url, content_type=CONTENT_TYPE_TEXT_PLAIN)

    async def check_updates(self) -> Any:
        url = f"{self._base_url}/check_updates.cgi"
        return await self._fetch(url)

    async def controller_error_logs(self) -> Any:
        url = f"{self._base_url}/cerror_logs.cgi"
        return await self._fetch(url, content_type=CONTENT_TYPE_TEXT_PLAIN)

    async def ftp_status(self) -> Any:
        url = f"{self._base_url}/ftp_status.cgi"
        return await self._fetch(url)

    async def id_interface(self, index: int) -> Any:
        params = {"index": index}
        url = f"{self._base_url}/id_interface.cgi"
        return await self._fetch(url, params)

    async def konnect_error_logs(self) -> Any:
        url = f"{self._base_url}/kerror_logs.cgi"
        return await self._fetch(url, content_type=CONTENT_TYPE_TEXT_PLAIN)

    async def languages(self) -> Any:
        url = f"{self._base_url}/languages.cgi"
        return await self._fetch(url)

    async def light_off(self, module: int) -> Any:
        params = {"module": module}
        url = f"{self._base_url}/light_off.cgi"
        return await self._fetch(url, params, content_type=CONTENT_TYPE_TEXT_PLAIN)

    async def light_on(self, module: int = 1, intensity: int = 100) -> Any:
        params = {"module": module, "intensity": intensity}
        url = f"{self._base_url}/light_on.cgi"
        return await self._fetch(url, params, content_type=CONTENT_TYPE_TEXT_PLAIN)

    async def light_module(self, module: int = 2, intensity: int = 100) -> Any:
        params = {"module": module, "intensity": intensity}
        url = f"{self._base_url}/light_module.cgi"
        return await self._fetch(url, params, content_type=CONTENT_TYPE_TEXT_PLAIN)

    async def massage_toggle(self) -> Any:
        url = f"{self._base_url}/massage_toggle.cgi"
        return await self._fetch(url)

    async def music_off(self, volume: int = 100) -> Any:
        params = {"volume": volume}
        url = f"{self._base_url}/music_off.cgi"
        return await self._fetch(url, params, content_type=CONTENT_TYPE_TEXT_PLAIN)

    async def music_on(self, volume: int = 100) -> Any:
        params = {"volume": volume}
        url = f"{self._base_url}/music_on.cgi"
        return await self._fetch(url, params, content_type=CONTENT_TYPE_TEXT_PLAIN)

    async def powerclean_check(self) -> Any:
        url = f"{self._base_url}/powerclean_check.cgi"
        return await self._fetch(url)

    async def rain_off(self) -> Any:
        url = f"{self._base_url}/rain_off.cgi"
        return await self._fetch(url, content_type=CONTENT_TYPE_TEXT_PLAIN)

    async def rain_on(
        self,
        *,
        color: int | None = None,
        effect: int | None = None,
    ) -> Any:
        if (color is None) == (effect is None):
            raise ValueError("Provide exactly one of 'color' or 'effect'")

        if color is not None:
            params: dict[str, Any] = {"mode": 1, "color": color}
        else:
            params = {"mode": 2, "effect": effect}

        url = f"{self._base_url}/rain_on.cgi"
        return await self._fetch(url, params, content_type=CONTENT_TYPE_TEXT_PLAIN)

    async def remove_module(self, module: int) -> Any:
        params = {"module": module}
        url = f"{self._base_url}/remove_module.cgi"
        return await self._fetch(url, params)

    async def reset_default(self) -> Any:
        url = f"{self._base_url}/reset_default.cgi"
        return await self._fetch(url)

    async def reset_controller_faults(self) -> Any:
        url = f"{self._base_url}/reset_cfault.cgi"
        return await self._fetch(url, content_type=CONTENT_TYPE_TEXT_PLAIN)

    async def reset_factory(self) -> Any:
        url = f"{self._base_url}/reset_factory.cgi"
        return await self._fetch(url, content_type=CONTENT_TYPE_TEXT_PLAIN)

    async def reset_konnect_faults(self) -> Any:
        url = f"{self._base_url}/reset_kfault.cgi"
        return await self._fetch(url, content_type=CONTENT_TYPE_TEXT_PLAIN)

    async def reset_users(self) -> Any:
        url = f"{self._base_url}/reset_users.cgi"
        return await self._fetch(url)

    async def save_default(self) -> Any:
        url = f"{self._base_url}/save_default.cgi"
        return await self._fetch(url)

    async def save_dt(self) -> Any:
        url = f"{self._base_url}/saveDT.cgi"
        return await self._fetch(url, content_type=CONTENT_TYPE_TEXT_PLAIN)

    async def save_ui(self, index: int) -> Any:
        params = {"index": index}
        url = f"{self._base_url}/saveUI.cgi"
        return await self._fetch(url, params)

    async def save_variable(self, index: int, value: int, **kwargs: Any) -> Any:
        params = {"index": index, "value": value}
        url = f"{self._base_url}/save_variable.cgi"
        return await self._fetch(url, {**kwargs, **params}, content_type=CONTENT_TYPE_TEXT_PLAIN)

    async def set_device(self, value: str) -> Any:
        url = f"{self._base_url}/set_device.cgi"
        return await self._fetch(url, {"value": value})

    async def steam_off(self) -> Any:
        url = f"{self._base_url}/steam_off.cgi"
        return await self._fetch(url, content_type=CONTENT_TYPE_TEXT_PLAIN)

    async def steam_on(self, temp: int = 110, time: int = 10) -> Any:
        params = {"temp": temp, "time": time}
        url = f"{self._base_url}/steam_on.cgi"
        return await self._fetch(url, params, content_type=CONTENT_TYPE_TEXT_PLAIN)

    async def stop_user(self) -> Any:
        url = f"{self._base_url}/stop_user.cgi"
        return await self._fetch(url, content_type=CONTENT_TYPE_TEXT_PLAIN)

    async def stop_shower(self) -> Any:
        url = f"{self._base_url}/stop_shower.cgi"
        return await self._fetch(url, content_type=CONTENT_TYPE_TEXT_PLAIN)

    async def start_user(self, user: int = 1) -> Any:
        params = {"user": user}
        url = f"{self._base_url}/start_user.cgi"
        return await self._fetch(url, params, content_type=CONTENT_TYPE_TEXT_PLAIN)

    async def swap_valves(self) -> Any:
        url = f"{self._base_url}/swapvalves.cgi"
        return await self._fetch(url)

    async def system_info(self) -> Any:
        url = f"{self._base_url}/system_info.cgi"
        return await self._fetch(url)

    async def upload_firmware(
        self,
        file_path: str | Path,
        timeout: float | None = None,
    ) -> Any:
        url = f"{self._base_url}/fileupload.cgi"
        return await self._post_file(url, file_path, timeout=timeout)

    async def values(self) -> Any:
        url = f"{self._base_url}/values.cgi"
        return await self._fetch(url)

    async def quick_shower(
        self,
        valve_num: int = 1,
        valve1_outlet: int = 1,
        valve1_massage: int = 0,
        valve1_temp: int = 100,
        valve2_outlet: int = 0,
        valve2_massage: int = 0,
        valve2_temp: int = 100,
    ) -> Any:
        params = {
            "valve_num": valve_num,
            "valve1_outlet": valve1_outlet,
            "valve1_massage": valve1_massage,
            "valve1_temp": valve1_temp,
            "valve2_outlet": valve2_outlet,
            "valve2_massage": valve2_massage,
            "valve2_temp": valve2_temp,
        }
        url = f"{self._base_url}/quick_shower.cgi"
        return await self._fetch(url, params, content_type=CONTENT_TYPE_TEXT_PLAIN)

    async def _fetch(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        content_type: str = CONTENT_TYPE_JSON,
        timeout: float | None = None,
    ) -> Any:
        """Send an async request to the Kohler device using raw asyncio streams."""
        timeout_val = timeout if timeout is not None else self.timeout
        path = urllib.parse.urlparse(url).path
        if params is not None:
            query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
            if query:
                path = f"{path}?{query}"

        req = f"GET {path} HTTP/1.1\r\nHost: {self._host}\r\nConnection: close\r\n\r\n"
        _LOGGER.debug("Sending request: GET %s", path)

        writer: asyncio.StreamWriter | None = None
        try:
            async with asyncio.timeout(timeout_val):
                reader, writer = await asyncio.open_connection(self._host, 80)
                writer.write(req.encode())
                await writer.drain()
                data = await reader.read()
            response_body = self._extract_response_body(data)
            response_text = response_body.decode("utf-8", errors="replace")
            _LOGGER.debug("Received response (%d bytes)", len(data))
        except (TimeoutError, OSError) as ex:
            _LOGGER.error("Connection failed while fetching %s: %s", path, ex)
            raise KohlerError(f"Connection failed: {ex}") from ex
        finally:
            if writer is not None:
                await self._close_writer(writer)

        if content_type == CONTENT_TYPE_JSON:
            try:
                return json.loads(response_text)
            except json.JSONDecodeError as ex:
                _LOGGER.error("Failed to parse JSON response: %s\nData: %s", ex, response_text)
                raise KohlerError(
                    f"Failed to parse JSON response: {ex}\nData: {response_text}"
                ) from ex
        return response_text

    async def _post_file(
        self,
        url: str,
        file_path: str | Path,
        timeout: float | None = None,
    ) -> Any:
        """Upload a file to the Kohler device asynchronously via POST."""
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"Firmware file not found: {path}")

        timeout_val = timeout if timeout is not None else max(self.timeout, 120.0)
        url_path = urllib.parse.urlparse(url).path
        boundary = f"----KohlerPythonBoundary{secrets.token_hex(16)}"
        _LOGGER.debug("Uploading file %s to %s", path, url_path)

        file_header = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="myfile"; filename="{path.name}"\r\n'
            f"Content-Type: application/octet-stream\r\n\r\n"
        )
        file_footer = f"\r\n--{boundary}--\r\n"
        content_length = len(file_header.encode()) + path.stat().st_size + len(file_footer.encode())

        req = (
            f"POST {url_path} HTTP/1.1\r\n"
            f"Host: {self._host}\r\n"
            f"Content-Type: multipart/form-data; boundary={boundary}\r\n"
            f"Content-Length: {content_length}\r\n"
            f"Connection: close\r\n\r\n"
        ).encode()

        writer: asyncio.StreamWriter | None = None
        try:
            async with asyncio.timeout(timeout_val):
                reader, writer = await asyncio.open_connection(self._host, 80)
                writer.write(req)
                writer.write(file_header.encode())
                with path.open("rb") as firmware_file:
                    while chunk := firmware_file.read(UPLOAD_CHUNK_SIZE):
                        writer.write(chunk)
                        await writer.drain()
                writer.write(file_footer.encode())
                await writer.drain()
                data = await reader.read()
            _LOGGER.debug("File upload complete (%d bytes received)", len(data))
            response_body = self._extract_response_body(data)
            return response_body.decode("utf-8", errors="replace")
        except (TimeoutError, OSError) as ex:
            _LOGGER.error("Upload failed: %s", ex)
            raise KohlerError(f"Upload failed: {ex}") from ex
        finally:
            if writer is not None:
                await self._close_writer(writer)

    async def _close_writer(self, writer: asyncio.StreamWriter) -> None:
        writer.close()
        with contextlib.suppress(OSError, TimeoutError):
            await asyncio.wait_for(writer.wait_closed(), timeout=1)

    def _extract_response_body(self, data: bytes) -> bytes:
        if not data.startswith(b"HTTP/"):
            return data

        try:
            header_block, body = data.split(b"\r\n\r\n", 1)
        except ValueError as ex:
            raise KohlerError("Malformed HTTP response: missing header separator") from ex

        header_lines = header_block.decode("iso-8859-1").split("\r\n")
        status_line = header_lines[0]
        status_parts = status_line.split(" ", 2)
        if len(status_parts) < 2 or not status_parts[1].isdigit():
            raise KohlerError(f"Malformed HTTP status line: {status_line}")

        status_code = int(status_parts[1])
        reason = status_parts[2] if len(status_parts) == 3 else ""
        headers: dict[str, str] = {}
        for header_line in header_lines[1:]:
            if not header_line:
                continue
            if ":" not in header_line:
                raise KohlerError(f"Malformed HTTP header: {header_line}")
            name, value = header_line.split(":", 1)
            headers[name.strip().lower()] = value.strip()

        transfer_encoding = headers.get("transfer-encoding", "").lower()
        if "chunked" in transfer_encoding:
            body = self._decode_chunked_body(body)
        elif "content-length" in headers:
            try:
                content_length = int(headers["content-length"])
            except ValueError as ex:
                raise KohlerError(
                    f"Malformed Content-Length header: {headers['content-length']}"
                ) from ex
            if len(body) < content_length:
                raise KohlerError(
                    "Incomplete HTTP response body: "
                    f"expected {content_length} bytes, got {len(body)}"
                )
            body = body[:content_length]

        if not 200 <= status_code < 300:
            status_text = f"HTTP {status_code}" if not reason else f"HTTP {status_code} {reason}"
            body_text = body.decode("utf-8", errors="replace").strip()
            if body_text:
                raise KohlerError(f"{status_text}: {body_text}")
            raise KohlerError(status_text)

        return body

    def _decode_chunked_body(self, body: bytes) -> bytes:
        decoded = bytearray()
        offset = 0

        while True:
            line_end = body.find(b"\r\n", offset)
            if line_end == -1:
                raise KohlerError("Malformed chunked response: missing chunk size terminator")

            chunk_size_line = body[offset:line_end]
            chunk_size_text = chunk_size_line.split(b";", 1)[0].decode("ascii")
            try:
                chunk_size = int(chunk_size_text, 16)
            except ValueError as ex:
                raise KohlerError(
                    f"Malformed chunked response: invalid chunk size {chunk_size_text!r}"
                ) from ex

            offset = line_end + 2
            if chunk_size == 0:
                return bytes(decoded)

            chunk_end = offset + chunk_size
            if len(body) < chunk_end + 2:
                raise KohlerError("Malformed chunked response: truncated chunk body")

            decoded.extend(body[offset:chunk_end])
            if body[chunk_end : chunk_end + 2] != b"\r\n":
                raise KohlerError("Malformed chunked response: missing chunk terminator")
            offset = chunk_end + 2

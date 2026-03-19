"""Tests for the Kohler DTV+ library."""

# ruff: noqa: E501
from __future__ import annotations

from typing import TYPE_CHECKING, Any
from unittest.mock import MagicMock, patch

if TYPE_CHECKING:
    from pathlib import Path

import pytest
import pytest_asyncio

from kohler import Kohler, KohlerError


@pytest_asyncio.fixture
async def kohler() -> Kohler:
    """Create a Kohler client instance for testing."""
    return Kohler(kohler_host="192.168.1.50")


class TestInit:
    """Tests for client initialization."""

    def test_base_url(self) -> None:
        kohler = Kohler("192.168.1.50")
        assert kohler._base_url == "http://192.168.1.50"
        assert kohler._host == "192.168.1.50"

    def test_custom_host(self) -> None:
        client = Kohler(kohler_host="kohler.local")
        assert client._base_url == "http://kohler.local"


# --- API Endpoint Parametrization ---

ENDPOINTS = [
    # method, kwargs, expected_path, expected_params, expected_kwargs (content_type, timeout)
    ("bt_disconnect", {}, "/bt_disconnect.cgi", None, {"content_type": "text/plain"}),
    ("check_updates", {}, "/check_updates.cgi", None, {}),
    ("controller_error_logs", {}, "/cerror_logs.cgi", None, {"content_type": "text/plain"}),
    ("ftp_status", {}, "/ftp_status.cgi", None, {}),
    ("id_interface", {"index": 2}, "/id_interface.cgi", {"index": 2}, {}),
    ("konnect_error_logs", {}, "/kerror_logs.cgi", None, {"content_type": "text/plain"}),
    ("languages", {}, "/languages.cgi", None, {}),
    ("light_off", {"module": 1}, "/light_off.cgi", {"module": 1}, {"content_type": "text/plain"}),
    ("light_on", {"module": 2, "intensity": 50}, "/light_on.cgi", {"module": 2, "intensity": 50}, {"content_type": "text/plain"}),
    ("light_module", {"module": 1, "intensity": 80}, "/light_module.cgi", {"module": 1, "intensity": 80}, {"content_type": "text/plain"}),
    ("massage_toggle", {}, "/massage_toggle.cgi", None, {}),
    ("music_off", {"volume": 0}, "/music_off.cgi", {"volume": 0}, {"content_type": "text/plain"}),
    ("music_on", {"volume": 80}, "/music_on.cgi", {"volume": 80}, {"content_type": "text/plain"}),
    ("powerclean_check", {}, "/powerclean_check.cgi", None, {}),
    ("rain_off", {}, "/rain_off.cgi", None, {"content_type": "text/plain"}),
    ("rain_on", {"color": 120}, "/rain_on.cgi", {"mode": 1, "color": 120}, {"content_type": "text/plain"}),
    ("rain_on", {"effect": 3}, "/rain_on.cgi", {"mode": 2, "effect": 3}, {"content_type": "text/plain"}),
    ("remove_module", {"module": 1}, "/remove_module.cgi", {"module": 1}, {}),
    ("reset_default", {}, "/reset_default.cgi", None, {}),
    ("reset_controller_faults", {}, "/reset_cfault.cgi", None, {"content_type": "text/plain"}),
    ("reset_factory", {}, "/reset_factory.cgi", None, {"content_type": "text/plain"}),
    ("reset_konnect_faults", {}, "/reset_kfault.cgi", None, {"content_type": "text/plain"}),
    ("reset_users", {}, "/reset_users.cgi", None, {}),
    ("save_default", {}, "/save_default.cgi", None, {}),
    ("save_dt", {}, "/saveDT.cgi", None, {"content_type": "text/plain"}),
    ("save_ui", {"index": 1}, "/saveUI.cgi", {"index": 1}, {}),
    ("save_variable", {"index": 1, "value": 2, "extra": "data"}, "/save_variable.cgi", {"index": 1, "value": 2, "extra": "data"}, {"content_type": "text/plain"}),
    ("set_device", {"value": "test"}, "/set_device.cgi", {"value": "test"}, {}),
    ("steam_off", {}, "/steam_off.cgi", None, {"content_type": "text/plain"}),
    ("steam_on", {"temp": 105, "time": 15}, "/steam_on.cgi", {"temp": 105, "time": 15}, {"content_type": "text/plain"}),
    ("stop_user", {}, "/stop_user.cgi", None, {"content_type": "text/plain"}),
    ("stop_shower", {}, "/stop_shower.cgi", None, {"content_type": "text/plain"}),
    ("start_user", {"user": 2}, "/start_user.cgi", {"user": 2}, {"content_type": "text/plain"}),
    ("swap_valves", {}, "/swapvalves.cgi", None, {}),
    ("system_info", {}, "/system_info.cgi", None, {}),
    ("values", {}, "/values.cgi", None, {}),
    ("quick_shower", {"valve_num": 1, "valve1_outlet": 2, "valve1_massage": 0, "valve1_temp": 100, "valve2_outlet": 0, "valve2_massage": 0, "valve2_temp": 100}, "/quick_shower.cgi", {"valve_num": 1, "valve1_outlet": 2, "valve1_massage": 0, "valve1_temp": 100, "valve2_outlet": 0, "valve2_massage": 0, "valve2_temp": 100}, {"content_type": "text/plain"})
]

class TestEndpoints:
    """Parametrized tests for all standard endpoints."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("method, kwargs, expected_path, expected_params, expected_kwargs", ENDPOINTS)
    async def test_endpoints(self, kohler: Kohler, method: str, kwargs: dict[str, Any], expected_path: str, expected_params: dict[str, Any] | None, expected_kwargs: dict[str, Any]) -> None:
        with patch.object(Kohler, "_fetch") as mock_fetch:
            mock_fetch.return_value = "OK"
            result = await getattr(kohler, method)(**kwargs)

            expected_url = f"http://192.168.1.50{expected_path}"
            if expected_params is None:
                mock_fetch.assert_called_once_with(expected_url, **expected_kwargs)
            else:
                mock_fetch.assert_called_once_with(expected_url, expected_params, **expected_kwargs)
            assert result == "OK"

    @pytest.mark.asyncio
    async def test_rain_on_validation(self, kohler: Kohler) -> None:
        with pytest.raises(ValueError, match="exactly one"):
            await kohler.rain_on(color=1, effect=2)
        with pytest.raises(ValueError, match="exactly one"):
            await kohler.rain_on()


class TestUploadFirmware:
    @pytest.mark.asyncio
    async def test_async_upload(self, kohler: Kohler, tmp_path: Path) -> None:
        fw_file = tmp_path / "firmware.bin"
        fw_file.write_bytes(b"\x00\x01\x02")
        with patch.object(Kohler, "_post_file") as mock_post:
            mock_post.return_value = "Upload OK"
            result = await kohler.upload_firmware(fw_file)
            assert result == "Upload OK"
            mock_post.assert_called_once_with("http://192.168.1.50/fileupload.cgi", fw_file)


class TestTransport:
    """Test the raw socket / asyncio streams transport implementations."""

    @pytest.mark.asyncio
    @patch("kohler.kohler.asyncio.open_connection")
    async def test_fetch_json(self, mock_open: MagicMock, kohler: Kohler) -> None:
        mock_reader = MagicMock()
        mock_writer = MagicMock()

        async def mock_read():
            return b'{"status": "ok"}'

        async def mock_dummy():
            pass

        mock_reader.read = mock_read
        mock_writer.drain = mock_dummy
        mock_writer.wait_closed = mock_dummy

        mock_open.return_value = (mock_reader, mock_writer)

        result = await kohler._fetch("http://192.168.1.50/test.cgi", {"p": 1})
        assert result == {"status": "ok"}

        req_bytes = mock_writer.write.call_args[0][0]
        assert b"GET /test.cgi?p=1 HTTP/1.1" in req_bytes

    @pytest.mark.asyncio
    @patch("kohler.kohler.asyncio.open_connection")
    async def test_fetch_timeout(self, mock_open: MagicMock, kohler: Kohler) -> None:
        mock_open.side_effect = TimeoutError()
        with pytest.raises(KohlerError, match="Connection failed"):
            await kohler._fetch("http://192.168.1.50/test")


class TestExports:
    def test_imports(self) -> None:
        from kohler import Kohler, KohlerError, __version__

        assert Kohler is not None
        assert KohlerError is not None
        assert isinstance(__version__, str)

    def test_kohler_error_is_exception(self) -> None:
        assert issubclass(KohlerError, Exception)

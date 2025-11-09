from src.endpoints.market_data_stream import MarketDataStream
from src.base_client import BaseAPIClient, BaseStreamClient
from unittest.mock import MagicMock, patch
import pytest


@patch("requests.get")
def test_make_request_refresh_token(mock_get):
    """Ensure token refresh on 401 works correctly."""
    mock_resp_401 = MagicMock(status_code=401)
    mock_resp_ok = MagicMock(status_code=200, json=lambda: {"ok": True})
    mock_get.side_effect = [mock_resp_401, mock_resp_ok]

    token_manager = MagicMock()
    token_manager.refresh_token.return_value = "newtok"

    api = BaseAPIClient(token_manager)
    res = api.make_request("url", {"Authorization": "Bearer X"}, {})
    assert res == {"ok": True}
    token_manager.refresh_token.assert_called_once()
    assert mock_get.call_count == 2


@patch.object(BaseStreamClient, "_run_stream")
def test_stream_loop_starts_and_stops(mock_run):
    """Ensure stream_loop runs once and stops when requested."""
    tm = MagicMock()
    client = BaseStreamClient(token_manager=tm)

    def stop_soon(*args, **kwargs):
        client._running = False
    mock_run.side_effect = stop_soon

    client.stream_loop("url", {}, {"Authorization": "t"}, MagicMock())
    mock_run.assert_called_once()


def test_refresh_and_reconnect_triggers_run_stream():
    """
    Ensure _refresh_and_reconnect refreshes token and recalls _run_stream.
    """
    tm = MagicMock()
    tm.refresh_token.return_value = "fresh"
    client = BaseStreamClient(token_manager=tm)
    client._run_stream = MagicMock()

    client._refresh_and_reconnect("url", {}, {}, MagicMock())
    tm.refresh_token.assert_called_once()
    client._run_stream.assert_called_once()


@patch.object(BaseStreamClient, "stream_loop")
def test_stream_bars_constructs_url_and_headers(mock_loop):
    """Ensure stream_bars builds correct URL, headers, and params."""
    tm = MagicMock()
    tm.get_token.return_value = "tok"
    api = MarketDataStream(token_manager=tm)

    api.stream_bars(symbol="AAPL", interval=5, unit="Minute", barsback=3)
    mock_loop.assert_called_once()

    call = mock_loop.call_args.kwargs
    assert "AAPL" in call["url"]
    assert call["params"]["interval"] == 5
    assert "Authorization" in call["headers"]
    assert "Accept" in call["headers"]
    assert "on_message" in call


def test_default_message_handler_logs():
    """Ensure default handler logs a valid bar message."""
    tm = MagicMock()
    api = MarketDataStream(token_manager=tm)

    api.logger = MagicMock()  # sostituisci il vero logger con un mock

    msg = {
        "TimeStamp": "2024-11-07T21:00:00Z",
        "Open": "1",
        "High": "2",
        "Low": "0.5",
        "Close": "1.5",
    }

    api._default_message_handler(msg)

    api.logger.info.assert_called_once()
    call_arg = api.logger.info.call_args[0][0]
    assert "O:1" in call_arg
    assert "C:1.5" in call_arg


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

# TODO: set dt_sent after self._que.get, not before self._que.put?

"""RAMSES RF - RAMSES-II compatible packet protocol finite state machine."""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Callable, Coroutine
from datetime import datetime as dt, timedelta as td
from queue import Empty, Full, PriorityQueue
from threading import Lock
from typing import TYPE_CHECKING, Any, Final

from . import exceptions as exc
from .address import HGI_DEV_ADDR
from .command import Command
from .const import MINIMUM_GAP_DURATION, SZ_ACTIVE_HGI, Priority
from .packet import Packet
from .typing import ExceptionT, QosParams

from .const import (  # noqa: F401, isort: skip, pylint: disable=unused-import
    I_,
    RP,
    RQ,
    W_,
    Code,
)

if TYPE_CHECKING:
    from .protocol import RamsesProtocolT
    from .transport import RamsesTransportT

_LOGGER = logging.getLogger(__name__)

# All debug flags should be False for end-users
_DBG_MAINTAIN_STATE_CHAIN = False  # maintain Context._prev_state


DEFAULT_MAX_BUFFER_SIZE: Final[int] = 32
DEFAULT_ECHO_TIMEOUT: Final[float] = 0.04  # waiting for echo pkt after cmd sent
DEFAULT_RPLY_TIMEOUT: Final[float] = 0.20  # waiting for reply pkt after echo pkt rcvd

_POLLING_INTERVAL: Final[float] = 0.0005


class _ProtocolWaitFailed(exc.ProtocolSendFailed):
    """The Command timed out when waiting for its turn to send."""


class _ProtocolEchoFailed(exc.ProtocolSendFailed):
    """The Command was sent OK, but failed to elicit its echo."""


class _ProtocolRplyFailed(exc.ProtocolSendFailed):
    """The Command received an echo OK, but failed to elicit the expected reply."""


class ProtocolContext:
    """To add state to a Protocol."""

    _proc_queue_task: None | asyncio.Task = None  # None when not connected to Protocol
    _state: _ProtocolStateT = None  # type: ignore[assignment]

    def __init__(
        self,
        protocol: RamsesProtocolT,
        /,
        *,
        max_buffer_size: int = DEFAULT_MAX_BUFFER_SIZE,
        echo_timeout: float = DEFAULT_ECHO_TIMEOUT,
        reply_timeout: float = DEFAULT_RPLY_TIMEOUT,
        min_gap_duration: float = MINIMUM_GAP_DURATION,
        max_retry_limit: int = 3,
    ) -> None:
        # super().__init__(*args, **kwargs)
        self._protocol = protocol
        self.max_buffer_size = max_buffer_size
        self.echo_timeout = td(seconds=echo_timeout)
        self.reply_timeout = td(seconds=reply_timeout)
        self.min_gap_duration = td(seconds=min_gap_duration)
        self.max_retry_limit = max_retry_limit

        self._loop = asyncio.get_running_loop()
        self._que: PriorityQueue = PriorityQueue(maxsize=self.max_buffer_size)
        self._mutex = Lock()

        self.set_state(Inactive)  # set initiate state, pre connection_made

    def __repr__(self) -> str:
        cls = self.state.__class__.__name__
        return (
            f"Context({cls}, len(Queue)="
            f"{self._que.unfinished_tasks}/{self._que._qsize()})"
        )

    def set_state(self, state: type[_ProtocolStateT]) -> None:
        """Set the State of the Protocol (context)."""

        prev_state = self._state

        # assert prev_state and prev_state._next_state is None  # FSM error

        if state in (Inactive, IsPaused, IsInIdle):
            self._state = state(self)

        else:  # if state in (WantEcho, WantRply, IsFailed):
            self._state = state(
                self,
                active_cmd=self._state.active_cmd,
                num_sends=self._state.num_sends,
                echo_frame=self._state._echo_frame,
                echo_pkt=self._state._echo_pkt,
            )

        # TODO: aquire lock
        if prev_state:
            prev_state._next_state = self._state  # used to detect transitions
        if _DBG_MAINTAIN_STATE_CHAIN:  # HACK for debugging
            setattr(self._state, "_prev_state", prev_state)  # noqa: B010
        # TODO: release lock

        if isinstance(self._state, IsInIdle | IsFailed):
            self._ensure_queue_processor()  # because just became Idle

    @property
    def state(self) -> _ProtocolStateT:
        return self._state

    def connection_made(self, transport: RamsesTransportT) -> None:
        self._proc_queue_task = self._loop.create_task(self._process_queued_cmds())
        self.state.made_connection(transport)  # TODO: needs to be after prev. line?

    def connection_lost(self, err: ExceptionT | None) -> None:
        fut: asyncio.Future

        self.state.lost_connection(err)

        if self._proc_queue_task:
            self._proc_queue_task.cancel()
            self._proc_queue_task = None  # FIXME

        # with self._que.mutex.acquire():
        while True:
            try:
                *_, fut = self._que.get_nowait()
            except Empty:
                break
            fut.cancel()

    def pause_writing(self) -> None:
        self.state.writing_paused()

    def resume_writing(self) -> None:
        self.state.writing_resumed()

    def pkt_received(self, pkt: Packet) -> None:
        # if isinstance(self.state, (WantEcho, WantRply)):  # not needed
        self.state.rcvd_pkt(pkt)

    async def send_cmd(
        self,
        send_fnc: Callable[[Command], Coroutine[Any, Any, None]],
        cmd: Command,
        priority: Priority,
        qos: QosParams,
    ) -> Packet:
        """Send the Command (with retries) and wait for the expected Packet.

        if wait_for_reply is True, wait for the RP/I corresponding to the RQ/W,
        otherwise simply return the echo Packet.

        Raises a ProtocolSendFailed if either max_retires or timeout is exceeded before
        receiving the expected packet.
        """

        def is_future_done(item: tuple) -> bool:
            """Return True if the item's Future is done (condition)."""
            fut: asyncio.Future  # mypy
            *_, fut = item
            return fut.done()  # usu. because expired?

        def remove_unwanted_items(queue: PriorityQueue, condition: Callable):
            """Removes all entries from the queue that satisfy the condition.."""
            # HACK: I have no idea if this is kosher (it does appear thread-safe)
            if queue.mutex.acquire():
                queue_copy = queue.queue[:]  # the queue attr is a list
                for entry in queue_copy:
                    if condition(entry):
                        queue.queue.remove(entry)
                queue.mutex.release()

        max_retries = qos.max_retries
        timeout = qos.timeout
        wait_for_reply = qos.wait_for_reply

        # if self.state.is_active_cmd(cmd):  # no need to queue?

        dt_sent = dt.now()  # TODO: put this after self._que.get?
        dt_expires = dt_sent + td(seconds=timeout)
        fut = self._loop.create_future()
        params = send_fnc, cmd, max_retries, wait_for_reply

        remove_unwanted_items(self._que, is_future_done)
        try:
            self._que.put_nowait(  # priority / dt_sent is the priority
                (priority, dt_sent, dt_expires, params, fut)
            )
        except Full:
            fut.set_exception(exc.ProtocolFsmError("Send queue full, cmd discarded"))

        self._ensure_queue_processor()  # because just added job to send queue

        try:
            pkt: Packet = await asyncio.wait_for(
                fut, timeout
            )  # TODO: return message instead?
        except TimeoutError as err:
            self.set_state(IsFailed)
            raise exc.ProtocolSendFailed(
                f"{cmd._hdr}: Timeout (outer) has expired"
            ) from err
        except exc.ProtocolError as err:
            self.set_state(IsFailed)
            raise exc.ProtocolSendFailed(f"{cmd._hdr}: Other error") from err

        self._ensure_queue_processor()  # because just completed job
        return pkt

    def _ensure_queue_processor(self) -> None:
        """Ensure the queue processor is running (called when a cmd is added)."""

        if self._mutex.acquire(timeout=0.005):
            if self._proc_queue_task is None:  # pkts sent before connection_made()?
                pass
            elif self._proc_queue_task.done():
                self._proc_queue_task = self._loop.create_task(
                    self._process_queued_cmds()
                )
            self._mutex.release()

    async def _process_queued_cmds(self) -> None:
        """Walk through the queue and send only the next valid Commands."""

        fut: asyncio.Future

        while True:
            try:
                *_, dt_expires, params, fut = self._que.get_nowait()
            except Empty:
                return

            if fut.done():
                self._que.task_done()
                continue

            if dt_expires <= dt.now():  # ?needed
                fut.set_exception(_ProtocolWaitFailed("Timeout (inner) has expired"))
                self._que.task_done()
                continue

            try:
                result = await self._send_cmd(*params)
            except exc.ProtocolSendFailed as err:
                fut.set_exception(err)
            else:
                fut.set_result(result)
            finally:
                self._que.task_done()
            break

    async def _send_cmd(  # actual Tx is in here
        self,
        send_fnc: Callable,
        cmd: Command,
        max_retries: int,
        wait_for_reply: bool | None,
    ) -> Packet:
        """Wrapper to send a command with retries, until success or exception.

        Supported Exceptions are limited to:
         - _ProtocolWaitFailed - issue sending Command
         - _ProtocolEchoFailed - issue receiving echo Packet
         - _ProtocolRplyFailed - issue receiving expected reply pPacket
        """

        if isinstance(self.state, IsFailed):  # is OK to send when last send failed
            self.set_state(IsInIdle)

        num_retries = -1
        while num_retries < max_retries:  # resend until RetryLimitExceeded
            num_retries += 1

            try:  # send the cmd
                # the order of these two calls appears irrelevent, but dev/tested as is
                self.state.sent_cmd(cmd)
                await send_fnc(cmd)  # the wrapped function (actual Tx.write)
                assert isinstance(self.state, WantEcho), f"{self}: Expects WantEcho"

            except (AssertionError, exc.ProtocolFsmError) as err:  # FIXME
                msg = f"{self}: Failed to Tx echo {cmd.tx_header}"
                if num_retries == max_retries:
                    raise _ProtocolWaitFailed(f"{msg}: {err}") from err
                _LOGGER.debug(f"{msg} (will retry): {err}")
                continue

            try:  # receive the echo pkt
                # assert isinstance(self.state, WantEcho)  # This won't work here
                prev_state, next_state = await self._wait_for_transition(
                    self.state,  # NOTE: is self.state, not next_state
                    self.echo_timeout + num_retries * self.min_gap_duration,
                )
                assert prev_state._echo_pkt, f"{self}: Missing echo packet"

                if not cmd.rx_header:  # no reply to wait for
                    # self.set_state(IsInIdle)  # FSM will do this
                    assert isinstance(next_state, IsInIdle), f"{self}: Expects IsInIdle"
                    return prev_state._echo_pkt

                if (
                    wait_for_reply is False
                    or (wait_for_reply is None and cmd.verb != RQ)
                    or cmd.code == Code._1FC9  # otherwise issues with binding FSM
                ):
                    # binding FSM is implemented at higher layer
                    self.set_state(IsInIdle)  # some will have been set to WantRply
                    assert isinstance(self.state, IsInIdle), f"{self}: Expects IsInIdle"
                    return prev_state._echo_pkt

                assert isinstance(next_state, WantRply), f"{self}: Expects WantRply"

            except (AssertionError, exc.ProtocolFsmError) as err:
                msg = f"{self}: Failed to Rx echo {cmd.tx_header}"
                if num_retries == max_retries:
                    raise _ProtocolEchoFailed(f"{msg}: {err}") from err
                _LOGGER.debug(f"{msg} (will retry): {err}")
                continue

            try:  # receive the reply pkt (if any)
                prev_state, next_state = await self._wait_for_transition(
                    next_state,  # NOTE: is next_state, not self.state
                    self.reply_timeout + num_retries * self.min_gap_duration,
                )
                assert isinstance(next_state, IsInIdle), f"{self}: Expects IsInIdle"
                assert prev_state._rply_pkt, f"{self}: Missing rply packet"

            except (AssertionError, exc.ProtocolFsmError) as err:
                msg = f"{self}: Failed to Rx reply {cmd.rx_header}"
                if num_retries == max_retries:
                    raise _ProtocolRplyFailed(f"{msg}: {err}") from err
                _LOGGER.debug(f"{msg} (will retry): {err}")
                continue

            return prev_state._rply_pkt

        # It would never be expected to reach this code, so a safety-net
        raise exc.ProtocolFsmError(f"{self}: Unexpected error {cmd.tx_header}")

    async def _wait_for_transition(
        self, this_state: _ProtocolStateT, timeout: td
    ) -> tuple[_ProtocolStateT, _ProtocolStateT]:
        until = dt.now() + timeout
        while until > dt.now():
            if this_state._next_state:
                break
            await asyncio.sleep(_POLLING_INTERVAL)
        else:
            raise exc.ProtocolFsmError(f"Failed to leave {this_state} in time")

        return this_state, this_state._next_state


class _ProtocolStateBase:
    """Protocol may Tx / can Rx according to it's internal state."""

    # state attrs
    active_cmd: None | Command
    num_sends: int

    _echo_frame: None | str = None
    _echo_pkt: None | Packet = None
    _rply_pkt: None | Packet = None

    _next_state: None | _ProtocolStateT = None  # used to detect transition

    _cant_send_cmd_error: None | str = "Not Implemented"

    def __init__(
        self,
        context: ProtocolContext,
        /,
        *,
        active_cmd: None | Command = None,
        num_sends: int = 0,
        echo_frame: None | str = None,
        echo_pkt: None | Packet = None,
    ) -> None:
        self._context = context  # a Protocol

        self.active_cmd = active_cmd  # #  the cmd as sent (the active cmd)
        self.num_sends = num_sends  # #    the number of times the active cmd was sent
        self._echo_frame = echo_frame  # # the expected echo Frame for the active cmd
        self._echo_pkt = echo_pkt  # #     the received echo Packet

    def __repr__(self) -> str:
        cls = self.__class__.__name__

        if isinstance(self, WantRply):
            assert self.active_cmd is not None
            return f"{cls}(rx_hdr={self.active_cmd.rx_header}, sends={self.num_sends})"

        if isinstance(self, WantEcho | IsFailed):
            assert self.active_cmd is not None
            return f"{cls}(tx_hdr={self.active_cmd.tx_header}, sends={self.num_sends})"

        assert self.active_cmd is None  # Inactive | IsPaused | IsInIdle
        assert self.num_sends == 0, f"{self}: num_sends != 0"
        return f"{cls}()"

    def is_active_cmd(self, cmd: Command) -> bool:
        """Return True if this cmd is the active cmd."""
        return bool(cmd and cmd is self.active_cmd)

    def made_connection(self, transport: RamsesTransportT) -> None:
        """Set the Context to IsInIdle (can Tx/Rx) or IsPaused."""

        if self._context._protocol._pause_writing:
            self._context.set_state(IsPaused)
        else:
            self._context.set_state(IsInIdle)

    def lost_connection(self, err: ExceptionT | None) -> None:
        """Set the Context to Inactive (can't Tx, will not Rx)."""
        self._context.set_state(Inactive)

    def writing_paused(self) -> None:
        """Set the Context to IsPaused (shouldn't Tx, might Rx)."""
        self._context.set_state(IsPaused)

    def writing_resumed(self) -> None:
        """Set the Context to IsInIdle (can Tx/Rx)."""
        self._context.set_state(IsInIdle)

    def rcvd_pkt(self, pkt: Packet) -> None:
        """Receive a Packet without complaint (most times this is OK)."""
        pass

    def sent_cmd(self, cmd: Command) -> None:  # raises exception
        """Send a packet if in the correct state."""
        # if self._cant_send_cmd_error:
        raise exc.ProtocolFsmError(
            f"{self}: Can't send {cmd._hdr}: {self._cant_send_cmd_error}"
        )


class Inactive(_ProtocolStateBase):
    """Protocol cannot Tx at all, and wont Rx (no active connection to a Transport)."""

    _cant_send_cmd_error = "Protocol has no connected Transport"


class IsPaused(_ProtocolStateBase):
    """Protocol cannot Tx at all, but may Rx (Transport has no capacity to Tx)."""

    _cant_send_cmd_error = "Protocol is paused"


class IsInIdle(_ProtocolStateBase):
    """Protocol can Tx next Command, may Rx (has no current Command)."""

    _cant_send_cmd_error = None

    # NOTE: unfortunately, the cmd's src / echo's src can be different:
    # RQ --- 18:000730 10:052644 --:------ 3220 005 0000050000  # RQ|10:048122|3220|05
    # RQ --- 18:198151 10:052644 --:------ 3220 005 0000050000  # RQ|10:048122|3220|05

    def sent_cmd(self, cmd: Command) -> None:
        """The Transport has possibly sent a Command."""

        assert self.active_cmd is None
        self.active_cmd = cmd

        # FIXME: the following requires the active GWY's device_id to be known...
        if self.active_cmd._frame[7:16] != HGI_DEV_ADDR.id:  # applies only for addr0
            self._echo_frame = self.active_cmd._frame

        elif src_id := self._context._protocol._transport.get_extra_info(SZ_ACTIVE_HGI):
            self._echo_frame = (
                self.active_cmd._frame[:7] + src_id + self.active_cmd._frame[16:]
            )

        else:
            self._echo_frame = self.active_cmd._frame

        self.num_sends = 1
        self._context.set_state(WantEcho)


class _WantPkt(_ProtocolStateBase):
    _cant_send_cmd_error = None

    def sent_cmd(self, cmd: Command) -> None:
        """The Transport has likely re-sent a Command."""

        if not self.is_active_cmd(cmd):
            raise exc.ProtocolFsmError(
                f"{self}: Can't send {cmd._hdr}: not active Command"
            )

        self._context.set_state(WantEcho)


class WantEcho(_WantPkt):
    """Protocol can re-Tx this Command, wanting a Rx (has an outstanding Command)."""

    def rcvd_pkt(self, pkt: Packet) -> None:
        """The Transport has possibly received the expected echo Packet."""

        assert isinstance(self.active_cmd, Command)  # mypy

        if pkt._frame != self._echo_frame:
            return

        self._echo_pkt = pkt
        if self.active_cmd.rx_header:  # and wait_for_reply is True:
            self._context.set_state(WantRply)
        else:
            self._context.set_state(IsInIdle)


class WantRply(_WantPkt):
    """Protocol can re-Tx this Command, wanting a Rx (has received echo)."""

    # NOTE: is possible get a false rply (same rx_header), e.g.:
    # RP --- 10:048122 18:198151 --:------ 3220 005 00C0050000  # 3220|RP|10:048122|05
    # RP --- 10:048122 01:145038 --:------ 3220 005 00C0050000  # 3220|RP|10:048122|05

    # NOTE: unfortunately, the cmd's src / rply's dst can still be different:
    # RQ --- 18:000730 10:052644 --:------ 3220 005 0000050000  # 3220|RQ|10:048122|05
    # RP --- 10:048122 18:198151 --:------ 3220 005 00C0050000  # 3220|RP|10:048122|05

    def rcvd_pkt(self, pkt: Packet) -> None:
        """The Transport has possibly received the expected response Packet."""

        assert isinstance(self.active_cmd, Command)  # mypy hint
        assert isinstance(self._echo_pkt, Packet)  # mypy hint

        # NOTE: use: pkt.dst.id !=     self._echo_pkt.src.id
        # and not:   pkt.dst    is not self._echo_pkt.src
        # because Addr may become Device from one packet to the next
        if pkt._hdr != self.active_cmd.rx_header or pkt.dst.id != self._echo_pkt.src.id:
            return

        self._rply_pkt = pkt
        self._context.set_state(IsInIdle)


class IsFailed(_ProtocolStateBase):
    """Protocol can't (yet) Tx next Command, but may Rx (last Command has failed)."""

    _cant_send_cmd_error = "Protocol FSM is in a failed state"


_ProtocolStateT = Inactive | IsPaused | IsInIdle | WantEcho | WantRply | IsFailed

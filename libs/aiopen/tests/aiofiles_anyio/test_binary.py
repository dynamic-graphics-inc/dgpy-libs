# -*- coding: utf-8 -*-
"""PEP 0492/Python 3.5+ tests for binary files."""

from __future__ import annotations

import io

from os import path
from typing import TYPE_CHECKING

import pytest

from aiopen import aiopen

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.anyio()
@pytest.mark.parametrize("mode", ["rb", "rb+", "ab+"])
@pytest.mark.parametrize("buffering", [-1, 0])
async def test_simple_iteration(mode: str, buffering: int) -> None:
    """Test iterating over lines from a file."""
    from aiopen import aiopen

    filename = path.join(path.dirname(__file__), "resources", "multiline_file.txt")

    async with aiopen(filename, mode=mode, buffering=buffering) as file:
        # Append mode needs us to seek.
        await file.seek(0)

        counter = 1
        # The old iteration pattern:
        while True:
            line = await file.readline()
            if not line:
                break
            assert line.strip() == b"line " + str(counter).encode()
            counter += 1

        counter = 1
        await file.seek(0)
        # The new iteration pattern:
        async for line in file:
            assert line.strip() == b"line " + str(counter).encode()
            counter += 1

    assert file.closed


@pytest.mark.anyio()
@pytest.mark.parametrize("mode", ["rb", "rb+", "ab+"])
@pytest.mark.parametrize("buffering", [-1, 0])
async def test_simple_readlines(mode: str, buffering: int) -> None:
    """Test the readlines functionality."""
    filename = path.join(path.dirname(__file__), "resources", "multiline_file.txt")

    with open(filename, mode="rb") as f:
        expected = f.readlines()

    async with aiopen(str(filename), mode=mode) as file:
        # Append mode needs us to seek.
        await file.seek(0)

        actual = await file.readlines()

    assert actual == expected


@pytest.mark.anyio()
@pytest.mark.parametrize("mode", ["rb+", "wb", "ab"])
@pytest.mark.parametrize("buffering", [-1, 0])
async def test_simple_flush(mode: str, buffering: int, tmp_path: Path) -> None:
    """Test flushing to a file."""
    filename = "file.bin"

    full_file = tmp_path.joinpath(filename)

    if "r" in mode:
        full_file.touch()  # Read modes want it to already exist.

    async with aiopen(str(full_file), mode=mode, buffering=buffering) as file:
        await file.write(b"0")  # Shouldn't flush.

        if buffering == -1:
            assert full_file.read_bytes() == b""
        else:
            assert full_file.read_bytes() == b"0"

        await file.flush()

        assert full_file.read_bytes() == b"0"


@pytest.mark.anyio()
@pytest.mark.parametrize("mode", ["rb+", "wb+", "ab+"])
async def test_simple_peek(mode: str, tmp_path: Path) -> None:
    """Test flushing to a file."""
    filename = "file.bin"

    full_file = tmp_path.joinpath(filename)
    full_file.write_bytes(b"0123456789")

    async with aiopen(str(full_file), mode=mode) as file:
        if "a" in mode:
            await file.seek(0)  # Rewind for append modes.

        peeked = await file.peek(1)

        # Technically it's OK for the peek to return less bytes than requested.
        if peeked:
            assert peeked.startswith(b"0")

            read = await file.read(1)

            assert peeked.startswith(read)


@pytest.mark.anyio()
@pytest.mark.parametrize("mode", ["rb", "rb+", "ab+"])
@pytest.mark.parametrize("buffering", [-1, 0])
async def test_simple_read(mode: str, buffering: int) -> None:
    """Just read some bytes from a test file."""
    filename = path.join(path.dirname(__file__), "resources", "multiline_file.txt")
    async with aiopen(filename, mode=mode, buffering=buffering) as file:
        await file.seek(0)  # Needed for the append mode.

        actual = await file.read()

        assert (await file.read()) == b""
    assert actual == open(filename, mode="rb").read()


@pytest.mark.anyio()
@pytest.mark.parametrize("mode", ["rb", "rb+", "ab+"])
@pytest.mark.parametrize("buffering", [-1, 0])
async def test_staggered_read(mode: str, buffering: int) -> None:
    """Read bytes repeatedly."""
    filename = path.join(path.dirname(__file__), "resources", "multiline_file.txt")
    async with aiopen(filename, mode=mode, buffering=buffering) as file:
        await file.seek(0)  # Needed for the append mode.

        actual = []
        while True:
            byte = await file.read(1)
            if byte:
                actual.append(byte)
            else:
                break

        assert (await file.read()) == b""

        expected = []
        with open(filename, mode="rb") as f:
            while True:
                byte = f.read(1)
                if byte:
                    expected.append(byte)
                else:
                    break

    assert actual == expected


@pytest.mark.anyio()
@pytest.mark.parametrize("mode", ["rb", "rb+", "ab+"])
@pytest.mark.parametrize("buffering", [-1, 0])
async def test_simple_seek(mode: str, buffering: int, tmp_path: Path) -> None:
    """Test seeking and then reading."""
    filename = "bigfile.bin"
    content = b"0123456789" * 4 * io.DEFAULT_BUFFER_SIZE

    full_file = tmp_path.joinpath(filename)
    full_file.write_bytes(content)

    async with aiopen(str(full_file), mode=mode, buffering=buffering) as file:
        await file.seek(4)

        assert (await file.read(1)) == b"4"


@pytest.mark.anyio()
@pytest.mark.parametrize("mode", ["wb", "rb", "rb+", "wb+", "ab", "ab+"])
@pytest.mark.parametrize("buffering", [-1, 0])
async def test_simple_close_ctx_mgr(mode: str, buffering: int, tmp_path: Path) -> None:
    """Open a file, read a byte, and close it."""
    filename = "bigfile.bin"
    content = b"0" * 4 * io.DEFAULT_BUFFER_SIZE

    full_file = tmp_path.joinpath(filename)
    full_file.write_bytes(content)

    async with aiopen(str(full_file), mode=mode, buffering=buffering) as file:
        assert not file.closed
        assert not file._file.closed

    assert file.closed
    assert file._file.closed


@pytest.mark.anyio()
@pytest.mark.parametrize("mode", ["wb", "rb", "rb+", "wb+", "ab", "ab+"])
@pytest.mark.parametrize("buffering", [-1, 0])
async def test_simple_close_no_ctx_mgr(
    mode: str, buffering: int, tmp_path: Path
) -> None:
    """Open a file, read a byte, and close it."""
    filename = "bigfile.bin"
    content = b"0" * 4 * io.DEFAULT_BUFFER_SIZE

    full_file = tmp_path.joinpath(filename)
    full_file.write_bytes(content)

    file = await aiopen(str(full_file), mode=mode, buffering=buffering)
    assert not file.closed
    assert not file._file.closed

    await file.close()

    assert file.closed
    assert file._file.closed


@pytest.mark.anyio()
@pytest.mark.parametrize("mode", ["rb", "rb+", "ab+"])
@pytest.mark.parametrize("buffering", [-1, 0])
async def test_simple_readinto(mode: str, buffering: int) -> None:
    """Test the readinto functionality."""
    filename = path.join(path.dirname(__file__), "resources", "multiline_file.txt")
    async with aiopen(filename, mode=mode, buffering=buffering) as file:
        await file.seek(0)  # Needed for the append mode.

        array = bytearray(4)
        bytes_read = await file.readinto(array)

        assert bytes_read == 4
        assert array == open(filename, mode="rb").read(4)


@pytest.mark.anyio()
@pytest.mark.parametrize("mode", ["rb+", "wb", "ab+"])
@pytest.mark.parametrize("buffering", [-1, 0])
async def test_simple_truncate(mode: str, buffering: int, tmp_path: Path) -> None:
    """Test truncating files."""
    filename = "bigfile.bin"
    content = b"0123456789" * 4 * io.DEFAULT_BUFFER_SIZE

    full_file = tmp_path.joinpath(filename)
    full_file.write_bytes(content)

    async with aiopen(str(full_file), mode=mode, buffering=buffering) as file:
        # The append modes want us to seek first.
        await file.seek(0)

        if "w" in mode:
            # We've just erased the entire file.
            await file.write(content)
            await file.flush()
            await file.seek(0)

        await file.truncate()

    assert full_file.read_bytes() == b""


@pytest.mark.anyio()
@pytest.mark.parametrize("mode", ["wb", "rb+", "wb+", "ab", "ab+"])
@pytest.mark.parametrize("buffering", [-1, 0])
async def test_simple_write(mode: str, buffering: int, tmp_path: Path) -> None:
    """Test writing into a file."""
    filename = "bigfile.bin"
    content = b"0" * 4 * io.DEFAULT_BUFFER_SIZE

    full_file = tmp_path.joinpath(filename)

    if "r" in mode:
        full_file.touch()  # Read modes want it to already exist.

    async with aiopen(str(full_file), mode=mode, buffering=buffering) as file:
        bytes_written = await file.write(content)

    assert bytes_written == len(content)
    assert content == full_file.read_bytes()


@pytest.mark.anyio()
async def test_simple_detach(tmp_path: Path) -> None:
    """Test detaching for buffered streams."""
    filename = "file.bin"

    full_file = tmp_path.joinpath(filename)
    full_file.write_bytes(b"0123456789")

    with pytest.raises(ValueError):
        async with aiopen(str(full_file), mode="rb") as file:
            raw_file = file.detach()

            assert raw_file

            with pytest.raises(ValueError):
                await file.read()

    assert raw_file.read(10) == b"0123456789"  # type: ignore[union-attr]


@pytest.mark.anyio()
async def test_simple_readall(tmp_path: Path) -> None:
    """Test the readall function by reading a large file in.

    Only RawIOBase supports readall().
    """
    filename = "bigfile.bin"
    content = b"0" * 4 * io.DEFAULT_BUFFER_SIZE  # Hopefully several reads.

    sync_file = tmp_path.joinpath(filename)
    sync_file.write_bytes(content)

    file = await aiopen(str(sync_file), mode="rb", buffering=0)

    actual = await file.readall()

    assert actual == content

    await file.close()
    assert file.closed

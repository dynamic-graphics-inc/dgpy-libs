from textwrap import dedent

from shellfish.done import Done, HrTime


class TestDoneReprStr:
    def test_str_done(self) -> None:
        d = Done(
            args=["python", "--version"],
            returncode=0,
            stdout="Python 3.13.5\n",
            stderr="",
            ti=1753910725.1278882,
            tf=1753910725.167228,
            dt=0.03933978080749512,
            hrdt=HrTime(secs=0, nanos=39339780),
            stdin=None,
            async_proc=False,
            verbose=False,
            dryrun=False,
        )
        expected_str = dedent(r"""
        Done(
            args=['python', '--version'],
            returncode=0,
            stdout='Python 3.13.5\n',
            stderr='',
            ti=1753910725.1278882,
            tf=1753910725.167228,
            dt=0.03933978080749512,
            hrdt={'secs': 0, 'nanos': 39339780},
            stdin=None,
            async_proc=False,
            verbose=False,
            dryrun=False,
        )
        """)
        assert str(d) == expected_str.strip()
        evaluated = eval(str(d))
        assert isinstance(evaluated, Done)
        assert evaluated == d

    def test_repr_done(self) -> None:
        d = Done(
            args=["python", "--version"],
            returncode=0,
            stdout="Python 3.13.5\n",
            stderr="",
            ti=1753910725.1278882,
            tf=1753910725.167228,
            dt=0.03933978080749512,
            hrdt=HrTime(secs=0, nanos=39339780),
            stdin=None,
            async_proc=False,
            verbose=False,
            dryrun=False,
        )
        expected_repr = dedent(r"""
        Done(args=['python', '--version'], returncode=0, stdout='Python 3.13.5\n', stderr='', ti=1753910725.1278882, tf=1753910725.167228, dt=0.03933978080749512, hrdt={'secs': 0, 'nanos': 39339780}, stdin=None, async_proc=False, verbose=False, dryrun=False)
        """)
        assert repr(d) == expected_repr.strip()

        evaluated = eval(repr(d))
        assert isinstance(evaluated, Done)
        assert evaluated == d

    def test_repr_done_multiline(self) -> None:
        d = Done(
            args=["python", "--version"],
            returncode=0,
            stdout="Python 3.13.5\n",
            stderr="",
            ti=1753910725.1278882,
            tf=1753910725.167228,
            dt=0.03933978080749512,
            hrdt=HrTime(secs=0, nanos=39339780),
            stdin=None,
            async_proc=False,
            verbose=False,
            dryrun=False,
        )
        expected_repr = dedent(r"""
        Done(args=['python', '--version'], returncode=0, stdout='Python 3.13.5\n', stderr='', ti=1753910725.1278882, tf=1753910725.167228, dt=0.03933978080749512, hrdt={'secs': 0, 'nanos': 39339780}, stdin=None, async_proc=False, verbose=False, dryrun=False)
        """)
        assert repr(d) == expected_repr.strip()

        evaluated = eval(repr(d))
        assert isinstance(evaluated, Done)
        assert evaluated == d

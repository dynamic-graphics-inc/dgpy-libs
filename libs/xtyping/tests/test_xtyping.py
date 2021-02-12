from xtyping import _xtyping


def test_xtyping_all():
    members = dir(_xtyping)
    a = _xtyping.__typing__
    non_typing_members = [
        el for el in members if el not in a and not el.startswith('__')
    ]
    xtyping_all = _xtyping.__all__

    if not all(el in xtyping_all for el in non_typing_members):
        print('shit')

        missing = sorted([el for el in non_typing_members if el not in xtyping_all])
        raise ValueError('MISSING from __all__: {}'.format('\n'.join(missing)))

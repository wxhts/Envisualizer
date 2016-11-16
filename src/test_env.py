def test_createWellIndex():
    from createWellIndex import createWellIndex

    indexed1 = createWellIndex('envision.csv')
    indexed2 = createWellIndex('envision.csv', reverse_row=True)

    assert 'Row' and 'Column' in list(indexed1.columns.values)
    assert 'Reverse Row' in list(indexed2.columns.values)

    wells = indexed1.loc[indexed1['Well'] == 'AA29']
    assert ((wells['Row'] == 27) & (wells['Column'] == 29)).any()


def test_createControls():
    from createControls import createControls
    test1 = createControls('controltest.csv')
    test2 = createControls('controltest.csv', standards=True)

    assert len(test1) == 2
    assert len(test2) == 3
    assert len(test1[0]) > 0
    assert len(test1[1]) > 0
    assert len(test2[2]) > 0


def test_CV():
    from createWellIndex import createWellIndex
    from envisualize import EnVisualize

    indexed = createWellIndex('envision.csv')
    env_obj = EnVisualize(indexed, 'controltest.csv')

    assert env_obj.CV('hpe') > 0
    assert env_obj.CV('zpe') > 0

    assert env_obj.CV('hpe') >= env_obj.CV('hpe', outlier=True)
    assert env_obj.CV('zpe') >= env_obj.CV('zpe', outlier=True)


def test_signalToBackground():
    from createWellIndex import createWellIndex
    from envisualize import EnVisualize

    indexed = createWellIndex('envision.csv')
    env_obj = EnVisualize(indexed, 'controltest.csv')
    env_obj.CV('hpe')
    env_obj.CV('zpe')

    assert env_obj.signalToBackground() > 0


def test_zPrime():
    from createWellIndex import createWellIndex
    from envisualize import EnVisualize

    indexed = createWellIndex('envision.csv')
    env_obj = EnVisualize(indexed, 'controltest.csv')
    env_obj.CV('hpe')
    env_obj.CV('zpe')

    assert 0 <= env_obj.zPrime() <= 1

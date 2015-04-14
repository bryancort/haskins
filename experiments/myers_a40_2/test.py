def foo():
    try:
        raise Exception(test)
    except:
        raise
    finally:
        return 1

a = foo()
print a
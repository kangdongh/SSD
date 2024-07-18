def fail_test():
    raise ValueError(f"This test must fail")


if __name__ == '__main__':
    try:
        fail_test()
    except Exception:
        print("FAIL")
        exit(-1)
    print("PASS")

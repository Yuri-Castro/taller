import unittest


def run_tests():
    loader = unittest.TestLoader()
    suite = loader.discover("tests")  # pasta de testes

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == "__main__":
    run_tests()

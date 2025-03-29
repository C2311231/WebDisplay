import tests, test_engine

engine = test_engine.Tester()

tests.add_tests(engine)

engine.run_tests()
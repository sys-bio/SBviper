# km_test: Testing Kinetics Models In Systems Biology

1. Testing model specifications. These tests do not require running simulation codes. An example is testing reaction specifications for mass balance.
2. Verifying simulation results. These tests analyze the results of simulation runs, such as whether the concentration of a chemical species converges to a particular value. The purpose of these checks is to verify that the model operates as the modeler intended.
3. An infrastructure for test execution and reuse. We find that some tests are applicable to many kinetics models. We have created an infrastructure that supports test reuse.

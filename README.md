These data files resulted from the paper [The tunnel number of all 11 and 12 crossing alternating knots (arXiv:1908.01693)](https://arxiv.org/abs/1908.01693).

* [montesinos.csv](./montesinos.csv) is a list of all Montesinos knots with 14 crossings or fewer (excluding rational knots).
* [tunnel.csv](./tunnel.csv) is a list of all knots with 12 crossings or less. It includes the tunnel number of all but 192 of these knots.

The following code was used to produce the above files. These scripts are written in either Python or SageMath, and some of them use the programs [SnapPy](https://www.math.uic.edu/t3m/SnapPy/) or [Heegaard](https://www.math.uic.edu/t3m/). Each folder in [code](./code) contains a script with its corresponding input (some taken from [KnotInfo](https://knotinfo.math.indiana.edu/) and [Knotorious](https://www.mimuw.edu.pl/~mcboro/knotorious.php)) and output files.

* [montesinoscode.txt](./code/montesinos/montesinoscode.txt) is a Python code that outputs a list of all Montesinos knots with 14 crossings or fewer (excluding rational knots).
* To obtain the tunnel number data, run the scripts [step1code.txt](./code/step1/step1code.txt) (Python), [step2code.txt](./code/step2/step2code.txt) (SageMath), [step3code.txt](./code/step3/step3code.txt) (SageMath), [step4code.txt](./code/step4/step4code.txt) (SageMath), [step5code.txt](./code/step5/step5code.txt) (SageMath), and [step6code.txt](./code/step6/step6code.txt) (SageMath) in this order.

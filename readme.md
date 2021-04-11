# port scanner

[github repository](https://github.com/loran-code/port_scanner/)

### Points of attention
- Threading has not been implemented yet but can be given as terminal input. It does nothing "extra" right now but has not been disabled as it would break other parts in the code.
- within pycharm when querying the database with an ip that does not exist within the database the program "hangs".
  within a terminal this does not happen and will return a valid error
- Once the scans are running it's not always possible to CTRL + C out of the program.
  - Wait for the scan to finish
  - Close the terminal


### setup / install
In the supplied text file `requirements.txt` are the used  libraries and packages.
However to my knowledge the amount of libraries is to much but I do not know how this may have happened.
Install the programs to your own knowledge.

The command `python -m pip freeze > requirements.txt` has been used

Advice is to make a virtual environment and install the packages from the requirements.txt file
- step 1: 
- step 2: `python -m pip install -r requirements.txt`


#### Required flags
-t Specify the IP address of the target. Either a hostname or IP can be given.

#### Optional flags
-p give a single port to scan

-pl give a list of ports to scan. e.g. 22 53 80 443

-pr give a range of ports to scan. e.g. 1 100

-to Give wait time before program continues to the next port when no reply from the target port has been given

-th Not implemented yet

-o save scan output to json and xml format

-db save scan output to sqlite database

-dbq Query the database by entering an ip address

-s Program announces by voice when the scan is finished. requires sound on

-tc TCP connect scan

-ts TCP SYN scan

-tx TCP XMAS scan

-us UDP scan

-knock Play knocking sounds during the scan. The full immersive port knocking experience. requires sound

-joke Tell a network related joke. requires sound

#### Must
- unit testen
- test code on kali

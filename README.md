# gr-microtelecom
GNU Radio 3.7 source module for Microtelecom Perseus 

In order to build GNU Radio and this module, the following, PyBombs based, procedure may be followed (Ubuntu 14.04 LTS).
A comprehensive manual of Pyboms is found here:

https://github.com/gnuradio/pybombs/


```
# make home current
cd /home/$USER

# clone and build Pybombs
git clone https://github.com/gnuradio/pybombs.git
cd pybombs
python setup.py build

# install pybombs in a local directory
export PYTHONPATH=/home/$USER/pybombs-install/lib/python2.7/site-packages/
python setup.py install --prefix /home/$USER/pybombs-install

#
# go there and start the installation
# all the GNU Radio and Microtelecom package will be installed in /home/$USER/gr
#
cd /home/$USER/pybombs-install/bin
./pybombs recipes add gr-recipes git+https://github.com/gnuradio/gr-recipes.git  
./pybombs recipes add gr-etcetera git+https://github.com/gnuradio/gr-etcetera.git
./pybombs prefix init /home/$USER/gr -a myprefix
# the following step lasts about one hour on my PC; your mileage can vary
./pybombs -p myprefix install gnuradio gr-microtelecom

# test it
cd /home/$USER/gr
. ./setup_env.sh
gnuradio-companion
```

Even if the above procedure install all the dependencies, including the libperseus-sdr,
if you are going to use Perseus on Linux for the first time,
it is highly reccomended that you do a test build of libperseus-sdr before you start the GNU Radio build procedure.
Follow the instructions found here:

https://github.com/amontefusco/libperseus-sdr/blob/master/README.md

cd ~/Work/software

#PYTABLES
PYTABLES=pytables-1.3.2
wget -nc http://kent.dl.sourceforge.net/sourceforge/pytables/$PYTABLES.tar.gz
tar xzf $PYTABLES.tar.gz
cd $PYTABLES
python setup.py build_ext --inplace
cd tables/tests
PYTHONPATH=$PYTHONPATH:../..
python test_all.py
cd ../..
sudo python setup.py install
cd ..

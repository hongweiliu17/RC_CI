echo "== second get the clean scripts =="
git clone git://git.app.eng.bos.redhat.com/content-delivery-qe
cd content-delivery-qe
echo "== run the cases of clean data =="
virtualenv --system-site-packages ~/testpython
. ~/testpython/bin/activate
pip install setuptools --upgrade
pip install funcsigs
# The test-requirements.txt from CD team does not specify the python lib version
# ET run the script against instance openstack server, it means it will install the latest package without version specified
# I have to specify the python lib with some specific verison to avoid errors
pip install pytest==3.3.0
pip install -r test-requirements.txt
# change the config
sed -i 's/QA_01/QA_e2e/g'  /workdir/content-delivery-qe/unit_tests/helpers/test_init.py
#change the user of ssh to pulp
sed -i 's/at_user/root/g'  ${CI3_WORKSPACE}/content-delivery-qe/unit_tests/helpers/constants.py
# disable some lines which bring some errors
sed -i 's/"errata"/#"errata"/g'  ${CI3_WORKSPACE}/content-delivery-qe/unit_tests/helpers/constants.py
sed -i 's/"pulp"/#"pulp"/g'  ${CI3_WORKSPACE}/content-delivery-qe/unit_tests/helpers/constants.py
# disable one useless testing types
sed -i "/clear_akamai_cdn/d" ${CI3_WORKSPACE}/content-delivery-qe/unit_tests/helpers/test_run_helper.py
echo "setuptools=="
# clean the pulp and pulp-docker data
cd ${CI3_WORKSPACE}/content-delivery-qe
py.test -v unit_tests/tests/clean_data.py::CleanData::test_clean_rhsm_pulp_data
py.test -v unit_tests/tests/clean_data.py::CleanData::test_clean_docker_pulp_data
echo "== The pulp env is clean =="

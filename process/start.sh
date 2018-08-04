cd ../GBDT
make
cd ../FM
make

cd ../process

pypy add_category.py
pypy statistics_feature.py
pypy statistics_infrequent.py
pypy statistics_user_appear.py
pypy data_prepare.py
pypy statistics_id.py
pypy category4gbdt.py

../GBDT/gbdt -d 5 -t 20 ../GBDT_test ../GBDT_train ../test_gbdt_out ../train_gbdt_out

pypy merge_gbdt.py
../FM/fm -k 8 -t 4 -l 0.00002 ../fm_test_app ../fm_train_app
../FM/fm -k 8 -t 10 -l 0.00003 ../fm_test_mobile ../fm_train_mobile
pypy combine_app_mobile.py ../fm_test_result ../fm_test_app.out ../fm_test_mobile.out

pypy submission.py

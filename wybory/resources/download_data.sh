#!/bin/bash
for i in {1..68}; do wget `echo "http://prezydent2000.pkw.gov.pl/gminy/gm-okr"$i".xls"`; done
for i in {1..68}; do wget `echo "http://prezydent2000.pkw.gov.pl/gminy/obwody/obw"$i".xls"`; done

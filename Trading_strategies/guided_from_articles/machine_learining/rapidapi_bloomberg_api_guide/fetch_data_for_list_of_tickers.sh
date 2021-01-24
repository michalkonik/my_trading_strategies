#!/bin/bash

xls2csv Revolut_ticker_test.xls | sed -e's/"//g' | while read l; do d=`echo "$l" | awk  '{print $2}'`; chrome "$d"; done


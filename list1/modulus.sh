#!/bin/bash
cd files
PUBLIC_INFO=$(openssl x509 -in ./cacertificate.pem -text -noout)
MODULUS=`echo "$PUBLIC_INFO" | grep Modulus: -A 4 | tail -4`
echo `echo $MODULUS | tr -cd [:alnum:]`

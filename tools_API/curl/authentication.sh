#!/usr/bin/env bash
curl -k -H "Content-Type: application/json" -X POST -d '{"username":"admin","password":"admin"}' https://*CHANGE_TO_URL*
curl -k -H "Authorization: Bearer *CHANGE_TO_JWT_TOKEN*" -X POST ***
curl -k -H "Authorization: Basic *CHANGE_TO_BASIC_TOKEN*" -X POST ***

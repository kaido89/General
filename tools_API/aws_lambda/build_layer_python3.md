# Commands to build Layer Jira python library.
# 1 - Firstly, create a lib folder
# CHANGE to Python3 package or library
PY_PACKAGE=CHANGE_TO_PIP3_NAME
ACC_ID=CHANGE_TO_AWS_ACCOUNT_ID
LIB_DIR=$PY_PACKAGE/python/lib/python3.7/site-packages
mkdir -p $LIB_DIR

# 2 - Install the library to LIB_DIR
pip3 install $PY_PACKAGE -t $LIB_DIR

# 3 - Zip all the dependencies to boto3-latest.zip
cd $PY_PACKAGE
zip -r ../$PY_PACKAGE .

# 4 - Publish the layer
aws lambda publish-layer-version --layer-name $PY_PACKAGE --zip-file fileb://$PY_PACKAGE.zip   
# The above should return an ARN for a layer in the form:
# "arn:aws:lambda:region:ACC_ID:layer:boto3-latest:1"

# 5 - Add the layer to the function's configuration
aws lambda update-function-configuration --function-name <my-function> --layers arn:aws:lambda:region:ACC_ID:layer:$PY_PACKAGE:1

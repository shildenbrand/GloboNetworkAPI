#!/bin/bash

# NETAPI_ODL
echo "Waiting for ODL to go up"

MAX_RETRY=30
SLEEP_TIME=10

ODL_READY=0
API_READY=0

for i in $(seq 1  ${MAX_RETRY}); do
    
    sleep ${SLEEP_TIME}
    docker exec ovs1 ovs-vsctl show | grep is_connected > /dev/null

    # If the port is open we continue with the script
    if [ "$?" -eq "0" ]; then
        echo "ODL server is ready";
        ODL_READY=1;
    fi

    API_READY=$(docker exec netapi_app echo $IAMREADY)
    if [ "$ODL_READY" -eq "1"]
        echo "API is ready";
    fi
    
    if [ "$ODL_READY" -eq "1" && "$API_READY" -eq "1"]
        echo "Going on with the tests";
        break;
    fi
    
    # When maximum retries is achieved we exit with an error message
    if [ "$i" -eq "${MAX_RETRY}" ]; then
        echo "Max retry achieved"
        exit 1;
    fi

    echo "Retrying ${i}.."
done



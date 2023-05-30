#!/bin/bash

#ip neigh | grep -i '00:0a:59:0.:..:..' | cut -f1,6 -d' '

ip neigh | grep -i '..:..:..:..:..:..' | cut -f1,6 -d' '
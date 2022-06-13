#!/bin/bash
gendef - $1.dll | sed -r -e 's|^_||' -e 's|@[1-9]+$||' > $1.def

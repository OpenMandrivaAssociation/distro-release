if [ -r /etc/sysconfig/system ]; then
    . /etc/sysconfig/system
    export META_CLASS
else
    export META_CLASS=unknown
fi

if ( -r /etc/sysconfig/system ) then
    eval set SECURITY=3;
set CLASS=beginner;
set LIBSAFE=no;
set META_CLASS=download;
    setenv META_CLASS download
else
    setenv META_CLASS unknown
endif

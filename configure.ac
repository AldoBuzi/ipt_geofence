AC_INIT([ipt_geofence],[1.0])
AC_LANG(C)

AC_PROG_CPP
AC_PROG_CXX

DATE=`date +%y%m%d`
VERSION="1.0"
RELEASE=`git log --pretty=oneline | wc -l`
GIT_BRANCH=`git branch --no-color|cut -d ' ' -f 2`
GIT_HASH=`git log --pretty=format:"%H (%ad)"|head -1`
MACHINE=`uname -m`
SYSTEM=`uname -s`

AC_DEFINE_UNQUOTED(PACKAGE_MACHINE, "$MACHINE", [Machine definition])


if [ test -f /usr/bin/lsb_release ]; then
   OSNAME=`/usr/bin/lsb_release -d|cut -d ':' -f 2| sed -e 's/^[[[:space:]]]*//'`
else
   OS="Unknown"
fi

AC_DEFINE_UNQUOTED(PACKAGE_OS, "$OSNAME", [Opeating system])
   
CFLAGS="${CFLAGS} -I/usr/local/include -I/opt/homebrew/include"
LDFLAGS="${LDFLAGS} -L/usr/local/lib -L/opt/homebrew/lib"

IPT_RELEASE="${VERSION}.${DATE}"
AC_DEFINE_UNQUOTED(IPT_RELEASE, "$IPT_RELEASE", [release version])

AC_LANG([C++])

AC_CHECK_LIB([curl], [curl_easy_perform], [LIBS="${LIBS} -lcurl"])
if test ${ac_cv_lib_curl_curl_easy_perform} = "no"; then
  echo "Please do apt-get install libcurl4-openssl-dev (http://curl.haxx.se/)"
  exit 1
fi

AC_CHECK_LIB([zmq], [zmq_socket_monitor])
if test "x$ac_cv_lib_zmq_zmq_socket_monitor" = xyes; then :
   LIBS="$LIBS -lzmq"
  AC_DEFINE_UNQUOTED(HAVE_ZMQ, 1, [ZMQ is present])
else
  echo "ERROR: ZMQ not present or too old"
  exit 1
fi

AC_CHECK_LIB(resolv, inet_aton)

if test $SYSTEM != "FreeBSD" && test $SYSTEM != "Darwin"; then
  AC_CHECK_HEADERS([libnetfilter_queue/libnetfilter_queue.h], AC_DEFINE_UNQUOTED(HAVE_NETFILTER, 1, [nfq is present]))

  if test "x$ac_cv_header_libnetfilter_queue_libnetfilter_queue_h" = xyes; then :
     LIBS="$LIBS -lnetfilter_queue -lnfnetlink"
  else
    echo "Please do apt-get install libnetfilter-queue-dev and try again"
    exit 0
  fi
else
  LIBS="$LIBS -lpcap"
  CXX="$CXX -fno-color-diagnostics"
fi

NTOPCLOUD_HOME="../ntopcloud"
if test -d "${NTOPCLOUD_HOME}"; then
  SSL_INC="`pkg-config --cflags libssl` -I/usr/include/openssl"
  SSL_LIB="`pkg-config --libs libssl` -lssl -lcrypto -lsodium"

  CFLAGS="${CFLAGS} -I${NTOPCLOUD_HOME} ${SSL_INC}"
  CXXFLAGS="${CXXFLAGS} -I${NTOPCLOUD_HOME} ${SSL_INC}"
  LIBS="${NTOPCLOUD_HOME}/libcloud.a ${LIBS} ${SSL_LIB}"

  if test -d /usr/include/json-c; then
    LIBS="${LIBS} -ljson-c"
  else
   echo "FATAL ERROR: Please apt install libjson-c-dev"
 fi

 AC_DEFINE(HAVE_NTOP_CLOUD, 1, [ntop cloud detected])
fi

dnl> GeoIP
AC_CHECK_LIB([maxminddb], [MMDB_lookup_sockaddr])
dnl> AC_CHECK_HEADERS([maxminddb.h])
dnl>if ! (test ".${ac_cv_lib_maxminddb_MMDB_lookup_sockaddr}" = ".yes" && test ".${ac_cv_header_maxminddb_h}" = ".yes"); then
if ! test ".${ac_cv_lib_maxminddb_MMDB_lookup_sockaddr}" = ".yes"; then
  echo "Please do apt-get install libmaxminddb-dev and try again"
  exit 0
fi

AC_CHECK_LIB([jsoncpp], [main])

if ! test ".${ac_cv_lib_jsoncpp_main}" = ".yes"; then
  echo "Please do apt-get install libjsoncpp-dev and try again"
  exit 0
fi

dnl nDPI
if ! test -f "$HOME/nDPI/src/lib/libndpi.a"; then :
  if ! test -f "..//nDPI/src/lib/libndpi.a"; then :
    echo "nDPI missing. Please do:"
    echo "- cd $HOME"
    echo "- git clone https://github.com/ntop/nDPI.git"
    echo "- cd nDPI"
    echo "- ./autogen.sh"
    echo "- make"
    echo ""
    echo "And run this configure again"
    exit 0
  else
    LIBS="$LIBS ../nDPI/src/lib/libndpi.a"
    INCS="$INCS -I ../nDPI/src/include"    
  fi
else
  LIBS="$LIBS $HOME/nDPI/src/lib/libndpi.a"
  INCS="$INCS -I $HOME/nDPI/src/include"
fi

LIBS="$LIBS -lpthread -lm"

EXTN=
if test $MACHINE = "x86_64"; then
   EXTN="amd64"
else
   if test $MACHINE = "i686"; then
     EXTN="i386"
   else
     if test $MACHINE = "aarch64"; then
       EXTN="arm64"
     fi
   fi
fi

AC_MSG_CHECKING([PF_RING nBPF])
NBPF_HOME=../PF_RING/userland/nbpf
LIBNBPF=${NBPF_HOME}/libnbpf.a

if test -f ${LIBNBPF}; then :
   LIBS="${LIBS} ${LIBNBPF}"
   AC_MSG_RESULT(yes)
else
   AC_MSG_RESULT(no)
fi

if test $SYSTEM == "FreeBSD" || test $SYSTEM == "Darwin"; then
   CXX=c++
fi

AC_SUBST(VERSION)
AC_SUBST(RELEASE)
AC_SUBST(SYSTEM)
AC_SUBST(IPT_RELEASE)
AC_SUBST(GIT_BRANCH)
AC_SUBST(GIT_HASH)
AC_SUBST(DATE)
AC_SUBST(EXTN)
AC_SUBST(LIBS)
AC_SUBST(INCS)

AC_CONFIG_HEADERS(config.h)
AC_CONFIG_FILES(Makefile)

AC_OUTPUT
